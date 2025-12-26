'use client';

import { useEffect, useRef } from 'react';
import { Layer, PresetType } from '@/lib/api';

// Re-export encoding functions from shared module for convenience
export { encodeLayers, decodeLayers, parseRecipeFromPath, encodeRecipeToPath } from '@/lib/recipe-encoding';

/**
 * URL State Interface - represents all syncable state
 */
export interface UrlState {
  preset?: PresetType;
  layers?: Layer[];
  sixWay?: boolean;
  autoRotate?: boolean;
}

/**
 * Hook to synchronize state with URL (legacy - kept for compatibility)
 * Note: The new path-based routing handles URL sync via router.replace
 *
 * @param state Current state to sync to URL
 * @param enabled Whether sync is enabled (disable during initial load)
 */
export function useUrlSync(
  state: UrlState,
  enabled: boolean = true
): void {
  const isFirstRender = useRef(true);

  useEffect(() => {
    // Skip first render to avoid overwriting URL params on load
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }

    if (!enabled) return;

    // No-op: URL sync is now handled by router.replace in HomeClient
  }, [state.layers, state.sixWay, state.autoRotate, enabled]);
}
