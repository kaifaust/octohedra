import { ImageResponse } from 'next/og';
import { list } from '@vercel/blob';

export const runtime = 'edge';

export const alt = 'Octohedra - Fractal Geometry';
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = 'image/png';

async function getScreenshotUrl(id: string): Promise<string | null> {
  try {
    const { blobs } = await list({ prefix: `shapes/${id}/` });
    const screenshotBlob = blobs.find(b => b.pathname.includes('/screenshot_') && b.pathname.endsWith('.png'));
    return screenshotBlob?.downloadUrl || null;
  } catch {
    return null;
  }
}

export default async function Image({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const screenshotUrl = await getScreenshotUrl(id);

  if (screenshotUrl) {
    // Fetch the stored screenshot
    const screenshotResponse = await fetch(screenshotUrl);
    const screenshotData = await screenshotResponse.arrayBuffer();

    return new ImageResponse(
      (
        <div
          style={{
            background: 'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%)',
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
              background: 'linear-gradient(to top, rgba(10, 10, 15, 0.9) 0%, rgba(10, 10, 15, 0.1) 40%, rgba(10, 10, 15, 0.3) 100%)',
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

  // Fallback to default image if shape not found
  const fallbackImageData = await fetch(
    new URL('../../../public/og-fractal.png', import.meta.url)
  ).then((res) => res.arrayBuffer());

  return new ImageResponse(
    (
      <div
        style={{
          background: 'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%)',
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
            background: 'linear-gradient(to top, rgba(10, 10, 15, 0.95) 0%, rgba(10, 10, 15, 0.3) 50%, rgba(10, 10, 15, 0.5) 100%)',
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
