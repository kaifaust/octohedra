import { Metadata } from 'next';
import { HomeClient } from '@/app/page';

interface PageProps {
  params: Promise<{ recipe: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { recipe } = await params;

  const url = `https://www.octohedra.com/r/${recipe}`;

  return {
    openGraph: {
      title: 'Octohedra',
      description: 'Fractal geometry generator - create and 3D print octahedral fractals',
      url,
      siteName: 'Octohedra',
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title: 'Octohedra',
      description: 'Fractal geometry generator - create and 3D print octahedral fractals',
    },
    alternates: {
      canonical: url,
    },
  };
}

export default async function RecipePage({ params }: PageProps) {
  const { recipe } = await params;

  // Pass the recipe to HomeClient which will decode and render it
  return <HomeClient initialRecipe={recipe} />;
}
