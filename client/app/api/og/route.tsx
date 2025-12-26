import { ImageResponse } from 'next/og';
import { NextRequest } from 'next/server';
import { list } from '@vercel/blob';
import { generateShapeId } from '@/lib/shapes';
import { decodeLayers } from '@/hooks/useUrlSync';

export const runtime = 'edge';

const size = {
  width: 1200,
  height: 630,
};

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

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const layersParam = searchParams.get('l');
  const sixWayParam = searchParams.get('6');

  // Try to find screenshot from recipe params
  let screenshotUrl: string | null = null;

  if (layersParam) {
    const layers = decodeLayers(layersParam);
    if (layers) {
      const sixWay = sixWayParam === '1';
      const shapeId = generateShapeId(layers, sixWay);
      screenshotUrl = await getScreenshotUrl(shapeId);
    }
  }

  if (screenshotUrl) {
    // Fetch the stored screenshot and use it as background
    const screenshotResponse = await fetch(screenshotUrl);
    const screenshotData = await screenshotResponse.arrayBuffer();

    return new ImageResponse(
      (
        <div
          style={{
            background:
              'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%)',
            width: '100%',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: 'system-ui, sans-serif',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {/* Shape screenshot as background */}
          <img
            src={screenshotData as unknown as string}
            alt=""
            style={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              opacity: 0.95,
            }}
          />

          {/* Gradient overlay for text readability */}
          <div
            style={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              background:
                'linear-gradient(to top, rgba(10, 10, 15, 0.9) 0%, rgba(10, 10, 15, 0.1) 40%, rgba(10, 10, 15, 0.3) 100%)',
            }}
          />

          {/* Content container */}
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              position: 'absolute',
              bottom: '60px',
            }}
          >
            {/* Title */}
            <div
              style={{
                fontSize: 56,
                fontWeight: 700,
                background: 'linear-gradient(90deg, #ffc4a3, #a3b5ff)',
                backgroundClip: 'text',
                color: 'transparent',
                marginBottom: '12px',
                letterSpacing: '-0.02em',
              }}
            >
              Octohedra
            </div>

            {/* Tagline */}
            <div
              style={{
                fontSize: 24,
                color: 'rgba(255, 255, 255, 0.8)',
                letterSpacing: '0.05em',
              }}
            >
              Fractal Geometry Generator
            </div>
          </div>
        </div>
      ),
      {
        ...size,
      }
    );
  }

  // Fallback to default image
  const fallbackImageData = await fetch(
    new URL('../../../public/og-fractal.png', import.meta.url)
  ).then((res) => res.arrayBuffer());

  return new ImageResponse(
    (
      <div
        style={{
          background:
            'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%)',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'system-ui, sans-serif',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <img
          src={fallbackImageData as unknown as string}
          alt=""
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            opacity: 0.9,
          }}
        />

        <div
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            background:
              'linear-gradient(to top, rgba(10, 10, 15, 0.95) 0%, rgba(10, 10, 15, 0.3) 50%, rgba(10, 10, 15, 0.5) 100%)',
          }}
        />

        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            position: 'absolute',
            bottom: '80px',
          }}
        >
          <div
            style={{
              fontSize: 72,
              fontWeight: 700,
              background: 'linear-gradient(90deg, #ffc4a3, #a3b5ff)',
              backgroundClip: 'text',
              color: 'transparent',
              marginBottom: '16px',
              letterSpacing: '-0.02em',
            }}
          >
            Octohedra
          </div>

          <div
            style={{
              fontSize: 28,
              color: 'rgba(255, 255, 255, 0.8)',
              letterSpacing: '0.05em',
            }}
          >
            Fractal Geometry Generator
          </div>
        </div>
      </div>
    ),
    {
      ...size,
    }
  );
}
