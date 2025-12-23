import { useState, useCallback } from 'react';
import { generateFractal, GenerateParams } from '@/lib/api';

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

  return { objData, isLoading, error, generate };
}
