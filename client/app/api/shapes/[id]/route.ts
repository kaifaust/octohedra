import { list } from '@vercel/blob';
import { NextRequest, NextResponse } from 'next/server';
import { StoredShape, decodeRecipe } from '@/lib/shapes';

// GET: Get a specific shape by ID
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  // Check for blob token
  if (!process.env.BLOB_READ_WRITE_TOKEN) {
    return NextResponse.json(
      { error: 'Blob storage not configured' },
      { status: 503 }
    );
  }

  try {
    const { id } = await params;

    // List blobs for this shape
    const { blobs } = await list({ prefix: `shapes/${id}/` });

    if (blobs.length === 0) {
      return NextResponse.json(
        { error: 'Shape not found' },
        { status: 404 }
      );
    }

    // Find screenshot file (contains encoded recipe in filename)
    const screenshotBlob = blobs.find(b => b.pathname.includes('/screenshot_') && b.pathname.endsWith('.png'));

    if (!screenshotBlob) {
      return NextResponse.json(
        { error: 'Shape screenshot not found' },
        { status: 404 }
      );
    }

    // Extract encoded recipe from pathname
    // Format: shapes/{id}/screenshot_{encodedRecipe}.png
    const match = screenshotBlob.pathname.match(/shapes\/([^/]+)\/screenshot_([^.]+)\.png/);
    if (!match) {
      return NextResponse.json(
        { error: 'Invalid shape format' },
        { status: 500 }
      );
    }

    const [, , encodedRecipe] = match;
    const recipe = decodeRecipe(encodedRecipe);
    if (!recipe) {
      return NextResponse.json(
        { error: 'Failed to decode shape recipe' },
        { status: 500 }
      );
    }

    // Find STL blob
    const stlBlob = blobs.find(b => b.pathname.endsWith('.stl'));

    const shape: StoredShape = {
      id,
      layers: recipe.layers,
      sixWay: recipe.sixWay,
      stlUrl: stlBlob?.downloadUrl || '',
      screenshotUrl: screenshotBlob.downloadUrl,
      createdAt: screenshotBlob.uploadedAt.toISOString(),
    };

    return NextResponse.json(shape);
  } catch (error) {
    console.error('Error fetching shape:', error);
    return NextResponse.json(
      { error: 'Failed to fetch shape' },
      { status: 500 }
    );
  }
}
