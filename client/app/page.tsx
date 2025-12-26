import { Metadata } from 'next';
import { HomeClient } from './home-client';

interface PageProps {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

export async function generateMetadata({ searchParams }: PageProps): Promise<Metadata> {
  const params = await searchParams;
  const layersParam = typeof params.l === 'string' ? params.l : undefined;
  const sixWayParam = typeof params['6'] === 'string' ? params['6'] : undefined;

  // Build the OG image URL with recipe params
  const ogImageParams = new URLSearchParams();
  if (layersParam) {
    ogImageParams.set('l', layersParam);
  }
  if (sixWayParam) {
    ogImageParams.set('6', sixWayParam);
  }

  const ogImageUrl = ogImageParams.toString()
    ? `/api/og?${ogImageParams.toString()}`
    : '/api/og';

  return {
    title: 'Octohedra',
    description: 'Fractal geometry generator - create and 3D print octahedral fractals',
    openGraph: {
      title: 'Octohedra',
      description: 'Fractal geometry generator - create and 3D print octahedral fractals',
      url: 'https://octohedra.com',
      siteName: 'Octohedra',
      type: 'website',
      images: [
        {
          url: ogImageUrl,
          width: 1200,
          height: 630,
          alt: 'Octohedra - Fractal Geometry',
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: 'Octohedra',
      description: 'Fractal geometry generator - create and 3D print octahedral fractals',
      images: [ogImageUrl],
    },
  };
}

export default function Home() {
  return <HomeClient />;
}
