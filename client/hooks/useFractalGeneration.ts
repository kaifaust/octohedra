import { useState, useCallback } from 'react';
import { generateFractal, getPresetRecipe, GenerateParams, Recipe, PresetType } from '@/lib/api';

export function useFractalGeneration() {
  const [objData, setObjData] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const generate = useCallback(async (params: GenerateParams) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await generateFractal(params);
      setObjData(data);
    } catch (e) {
      setError(e instanceof Error ? e : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchPresetRecipe = useCallback(async (
    preset: PresetType,
    depth: number = 3,
    fillDepth: number = 0,
    stackHeight: number = 1
  ): Promise<Recipe | null> => {
    try {
      return await getPresetRecipe(preset, depth, fillDepth, stackHeight);
    } catch (e) {
      setError(e instanceof Error ? e : new Error('Unknown error'));
      return null;
    }
  }, []);

  return { objData, isLoading, error, generate, fetchPresetRecipe };
}
