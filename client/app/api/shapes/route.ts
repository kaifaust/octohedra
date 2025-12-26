import { put, list } from '@vercel/blob';
import { NextRequest, NextResponse } from 'next/server';
import { StoredShape, generateShapeId, encodeRecipe, decodeRecipe } from '@/lib/shapes';
import { Layer } from '@/lib/api';

// POST: Save a new shape with screenshot
export async function POST(request: NextRequest) {
  // Check for blob token
  if (!process.env.BLOB_READ_WRITE_TOKEN) {
    return NextResponse.json(
      { error: 'Blob storage not configured' },
      { status: 503 }
    );
  }

  try {
    const formData = await request.formData();

    const layersJson = formData.get('layers') as string;
    const sixWay = formData.get('sixWay') === 'true';
    const screenshot = formData.get('screenshot') as Blob;
    const stl = formData.get('stl') as Blob | null;

    if (!layersJson || !screenshot) {
      return NextResponse.json(
        { error: 'Missing required fields: layers and screenshot' },
        { status: 400 }
      );
    }

    const layers: Layer[] = JSON.parse(layersJson);
    const shapeId = generateShapeId(layers, sixWay);
    const recipeEncoded = encodeRecipe(layers, sixWay);

    // Check if shape already exists by listing blobs with this prefix
    const existingBlobs = await list({ prefix: `shapes/${shapeId}/` });
    if (existingBlobs.blobs.length > 0) {
      // Shape already exists, return existing URLs
      const screenshotBlob = existingBlobs.blobs.find(b => b.pathname.includes('/screenshot_'));
      const stlBlob = existingBlobs.blobs.find(b => b.pathname.endsWith('.stl'));

      if (screenshotBlob) {
        const shape: StoredShape = {
          id: shapeId,
          layers,
          sixWay,
          stlUrl: stlBlob?.downloadUrl || '',
          screenshotUrl: screenshotBlob.downloadUrl,
          createdAt: screenshotBlob.uploadedAt.toISOString(),
        };
        return NextResponse.json(shape);
      }
    }

    // Upload screenshot with recipe encoded in filename
    // Format: shapes/{id}/screenshot_{encodedRecipe}.png
    const screenshotBlob = await put(
      `shapes/${shapeId}/screenshot_${recipeEncoded}.png`,
      screenshot,
      { access: 'public', contentType: 'image/png' }
    );

    // Upload STL if provided
    let stlUrl = '';
    if (stl) {
      const stlBlob = await put(
        `shapes/${shapeId}/model.stl`,
        stl,
        { access: 'public', contentType: 'application/octet-stream' }
      );
      stlUrl = stlBlob.downloadUrl;
    }

    const metadata: StoredShape = {
      id: shapeId,
      layers,
      sixWay,
      stlUrl,
      screenshotUrl: screenshotBlob.downloadUrl,
      createdAt: new Date().toISOString(),
    };

    return NextResponse.json(metadata);
  } catch (error) {
    console.error('Error saving shape:', error);
    return NextResponse.json(
      { error: 'Failed to save shape' },
      { status: 500 }
    );
  }
}

// GET: List recent shapes
export async function GET(request: NextRequest) {
  // Check for blob token
  if (!process.env.BLOB_READ_WRITE_TOKEN) {
    return NextResponse.json(
      { error: 'Blob storage not configured' },
      { status: 503 }
    );
  }

  try {
    const searchParams = request.nextUrl.searchParams;
    const limit = parseInt(searchParams.get('limit') || '10', 10);

    // List all blobs
    const { blobs } = await list({ prefix: 'shapes/' });

    // Filter to screenshot files (which contain the encoded recipe)
    const screenshotBlobs = blobs.filter(b => b.pathname.includes('/screenshot_') && b.pathname.endsWith('.png'));

    // Sort by upload date (most recent first)
    screenshotBlobs.sort((a, b) =>
      new Date(b.uploadedAt).getTime() - new Date(a.uploadedAt).getTime()
    );

    // Take only the requested limit
    const recentBlobs = screenshotBlobs.slice(0, limit);

    // Build shapes from blob pathnames (no HTTP fetch needed!)
    const shapes: StoredShape[] = [];
    for (const blob of recentBlobs) {
      try {
        // Extract shape ID and encoded recipe from pathname
        // Format: shapes/{id}/screenshot_{encodedRecipe}.png
        const match = blob.pathname.match(/shapes\/([^/]+)\/screenshot_([^.]+)\.png/);
        if (!match) continue;

        const [, shapeId, encodedRecipe] = match;
        const recipe = decodeRecipe(encodedRecipe);
        if (!recipe) continue;

        // Find STL blob for this shape
        const stlBlob = blobs.find(b => b.pathname === `shapes/${shapeId}/model.stl`);

        shapes.push({
          id: shapeId,
          layers: recipe.layers,
          sixWay: recipe.sixWay,
          stlUrl: stlBlob?.downloadUrl || '',
          screenshotUrl: blob.downloadUrl,
          createdAt: blob.uploadedAt.toISOString(),
        });
      } catch (err) {
        console.error('Failed to parse shape from blob:', blob.pathname, err);
        // Skip this shape and continue
      }
    }

    return NextResponse.json(shapes);
  } catch (error) {
    console.error('Error listing shapes:', error);
    return NextResponse.json(
      { error: 'Failed to list shapes' },
      { status: 500 }
    );
  }
}
