import { HomeClient } from '@/app/page';

interface PageProps {
  params: Promise<{ recipe: string }>;
}

export default async function RecipePage({ params }: PageProps) {
  const { recipe } = await params;

  // Pass the recipe to HomeClient which will decode and render it
  return <HomeClient initialRecipe={recipe} />;
}
