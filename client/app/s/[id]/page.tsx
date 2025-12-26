import { Metadata } from 'next';
import { list } from '@vercel/blob';
import { StoredShape } from '@/lib/shapes';
import { encodeLayers } from '@/hooks/useUrlSync';
import { RedirectClient } from './redirect-client';

interface PageProps {
  params: Promise<{ id: string }>;
}

async function getShape(id: string): Promise<StoredShape | null> {
  try {
    const { blobs } = await list({ prefix: `shapes/${id}/` });
    const metadataBlob = blobs.find(b => b.pathname.endsWith('metadata.json'));

    if (!metadataBlob) return null;

    const response = await fetch(metadataBlob.url);
    return response.json();
  } catch {
    return null;
  }
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { id } = await params;

  return {
    title: 'Octohedra - Shared Fractal',
    description: 'Check out this fractal geometry I created with Octohedra',
    openGraph: {
      title: 'Octohedra - Shared Fractal',
      description: 'Check out this fractal geometry I created with Octohedra',
      url: `https://octohedra.com/s/${id}`,
      siteName: 'Octohedra',
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title: 'Octohedra - Shared Fractal',
      description: 'Check out this fractal geometry I created with Octohedra',
    },
  };
}

export default async function ShapePage({ params }: PageProps) {
  const { id } = await params;
  const shape = await getShape(id);

  if (!shape) {
    return <RedirectClient to="/" />;
  }

  // Build redirect URL for client-side navigation
  const layersParam = encodeLayers(shape.layers);
  const sixWayParam = shape.sixWay ? '&6=1' : '';
  const redirectUrl = `/?l=${layersParam}${sixWayParam}`;

  return <RedirectClient to={redirectUrl} />;
}
