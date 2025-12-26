import { redirect } from 'next/navigation';
import { list } from '@vercel/blob';
import { StoredShape } from '@/lib/shapes';
import { encodeLayers } from '@/hooks/useUrlSync';

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

export default async function ShapePage({ params }: PageProps) {
  const { id } = await params;
  const shape = await getShape(id);

  if (!shape) {
    redirect('/');
  }

  // Redirect to main page with recipe in URL
  const layersParam = encodeLayers(shape.layers);
  const sixWayParam = shape.sixWay ? '&6=1' : '';
  redirect(`/?l=${layersParam}${sixWayParam}`);
}
