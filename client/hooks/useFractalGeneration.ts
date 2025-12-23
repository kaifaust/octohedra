import { useState, useCallback } from 'react';
import { generateFractal, getPresetRecipe, GenerateParams, Recipe, PresetType } from '@/lib/api';

// Format bytes to human readable string
function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(i > 0 ? 1 : 0)} ${sizes[i]}`;
}

export function useFractalGeneration() {
  const [objData, setObjData] = useState<string | null>(null);
  const [fileSize, setFileSize] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const generate = useCallback(async (params: GenerateParams) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await generateFractal(params);
      setObjData(data);
      setFileSize(formatBytes(new Blob([data]).size));
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

  return { objData, fileSize, isLoading, error, generate, fetchPresetRecipe };
}
