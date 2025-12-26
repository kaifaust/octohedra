import { ImageResponse } from 'next/og';
import { list } from '@vercel/blob';
import { generateShapeId } from '@/lib/shapes';

export const runtime = 'edge';

export const alt = 'Octohedra - Fractal Geometry Generator';
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = 'image/png';

// Default shape ID (3f recipe)
const DEFAULT_SHAPE_ID = generateShapeId([{ depth: 3, shape: 'fractal' }], false);

async function getScreenshotUrl(shapeId: string): Promise<string | null> {
  try {
    const { blobs } = await list({ prefix: `shapes/${shapeId}/` });
    const screenshotBlob = blobs.find(
      (b) => b.pathname.includes('/screenshot_') && b.pathname.endsWith('.png')
    );
    return screenshotBlob?.downloadUrl || null;
  } catch {
    return null;
  }
}

export default async function Image() {
  const screenshotUrl = await getScreenshotUrl(DEFAULT_SHAPE_ID);

  if (screenshotUrl) {
    const screenshotResponse = await fetch(screenshotUrl);
    const screenshotData = await screenshotResponse.arrayBuffer();

    return new ImageResponse(
      (
        <div
          style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#000000',
          }}
        >
          <img
            src={screenshotData as unknown as string}
            alt=""
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'contain',
            }}
          />
        </div>
      ),
      {
        ...size,
      }
    );
  }

  // Fallback: black background with text (only if no screenshot available)
  return new ImageResponse(
    (
      <div
        style={{
          backgroundColor: '#000000',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'system-ui, sans-serif',
        }}
      >
        <div
          style={{
            fontSize: 72,
            fontWeight: 700,
            background: 'linear-gradient(90deg, #ffc4a3, #a3b5ff)',
            backgroundClip: 'text',
            color: 'transparent',
            letterSpacing: '-0.02em',
          }}
        >
          Octohedra
        </div>
      </div>
    ),
    {
      ...size,
    }
  );
}
