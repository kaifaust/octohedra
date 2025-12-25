'use client';

import { useCallback, useEffect, useRef } from 'react';
import { Layer, PresetType, LayerShape, SpawnDirection } from '@/lib/api';

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
 * Compact layer encoding format:
 * {depth}{shape}[.{spawns}][.{flags}]
 *
 * Shape: f=fractal, s=solid
 * Spawns: o=out, i=in, d=side (using 'd' to avoid conflict with 's' for solid)
 * Flags: b=bloom, e=echo
 *
 * Examples:
 * - "3f" = depth 3, fractal, no spawn
 * - "2f.oid" = depth 2, fractal, spawn out+in+side
 * - "2f.o.b" = depth 2, fractal, spawn out, bloom
 * - "1s" = depth 1, solid
 *
 * Multiple layers separated by "-":
 * - "3f-2f.o-1f" = 3 layers
 */

const SHAPE_CODES: Record<LayerShape, string> = { fractal: 'f', solid: 's' };
const SHAPE_DECODE: Record<string, LayerShape> = { f: 'fractal', s: 'solid' };

const SPAWN_CODES: Record<SpawnDirection, string> = { out: 'o', in: 'i', side: 'd' };
const SPAWN_DECODE: Record<string, SpawnDirection> = { o: 'out', i: 'in', d: 'side' };

/**
 * Encode a single layer to compact string format
 */
function encodeLayer(layer: Layer): string {
  const parts: string[] = [];

  // Depth + shape (required)
  const shape = SHAPE_CODES[layer.shape || 'fractal'];
  parts.push(`${layer.depth}${shape}`);

  // Spawns (optional)
  if (layer.spawn && layer.spawn.length > 0) {
    const spawns = layer.spawn.map(s => SPAWN_CODES[s]).sort().join('');
    parts.push(spawns);

    // Flags (only if spawns exist)
    const flags: string[] = [];
    if (layer.bloom) flags.push('b');
    if (layer.echo) flags.push('e');
    if (flags.length > 0) {
      parts.push(flags.join(''));
    }
  }

  return parts.join('.');
}

/**
 * Decode a compact string to a layer
 */
function decodeLayer(encoded: string): Layer | null {
  try {
    const parts = encoded.split('.');
    if (parts.length === 0) return null;

    // Parse depth and shape from first part
    const match = parts[0].match(/^(\d)([fs])$/);
    if (!match) return null;

    const depth = parseInt(match[1], 10);
    const shape = SHAPE_DECODE[match[2]];

    if (depth < 1 || depth > 5 || !shape) return null;

    const layer: Layer = { depth, shape };

    // Parse spawns (second part if exists)
    if (parts.length > 1 && parts[1]) {
      const spawns: SpawnDirection[] = [];
      for (const char of parts[1]) {
        const spawn = SPAWN_DECODE[char];
        if (spawn) spawns.push(spawn);
      }
      if (spawns.length > 0) {
        layer.spawn = spawns;
      }
    }

    // Parse flags (third part if exists)
    if (parts.length > 2 && parts[2] && layer.spawn) {
      if (parts[2].includes('b')) layer.bloom = true;
      if (parts[2].includes('e')) layer.echo = true;
    }

    return layer;
  } catch {
    return null;
  }
}

/**
 * Encode layers array to URL-safe string
 */
export function encodeLayers(layers: Layer[]): string {
  return layers.map(encodeLayer).join('-');
}

/**
 * Decode URL string to layers array
 */
export function decodeLayers(encoded: string): Layer[] | null {
  try {
    if (!encoded) return null;

    const layerStrings = encoded.split('-');
    const layers: Layer[] = [];

    for (const str of layerStrings) {
      const layer = decodeLayer(str);
      if (!layer) return null;
      layers.push(layer);
    }

    return layers.length > 0 ? layers : null;
  } catch {
    return null;
  }
}

/**
 * Valid presets for validation
 */
const VALID_PRESETS = new Set<PresetType>(['flake', 'tower', 'evil_tower', 'flower', 'temple_complex']);

/**
 * Parse URL search params into UrlState
 */
export function parseUrlState(searchParams: URLSearchParams): UrlState {
  const state: UrlState = {};

  // Parse preset
  const preset = searchParams.get('p');
  if (preset && VALID_PRESETS.has(preset as PresetType)) {
    state.preset = preset as PresetType;
  }

  // Parse layers (overrides preset)
  const layersParam = searchParams.get('l');
  if (layersParam) {
    const layers = decodeLayers(layersParam);
    if (layers) {
      state.layers = layers;
    }
  }

  // Parse six-way
  const sixWay = searchParams.get('6');
  if (sixWay !== null) {
    state.sixWay = sixWay === '1';
  }

  // Parse auto-rotate
  const rotate = searchParams.get('r');
  if (rotate !== null) {
    state.autoRotate = rotate === '1';
  }

  return state;
}

/**
 * Build URL search params from state
 */
export function buildUrlParams(state: UrlState): URLSearchParams {
  const params = new URLSearchParams();

  // Always encode layers for shareable URLs
  if (state.layers && state.layers.length > 0) {
    params.set('l', encodeLayers(state.layers));
  }

  // Add six-way if true
  if (state.sixWay) {
    params.set('6', '1');
  }

  // Add auto-rotate if false (default is true)
  if (state.autoRotate === false) {
    params.set('r', '0');
  }

  return params;
}

/**
 * Hook to synchronize state with URL
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

    const params = buildUrlParams(state);
    const newUrl = params.toString()
      ? `${window.location.pathname}?${params.toString()}`
      : window.location.pathname;

    // Use replaceState to avoid polluting browser history
    window.history.replaceState(null, '', newUrl);
  }, [state.layers, state.sixWay, state.autoRotate, enabled]);
}

/**
 * Get initial state from URL on page load
 * Call this once on mount before setting up state
 */
export function getInitialUrlState(): UrlState {
  if (typeof window === 'undefined') return {};

  const searchParams = new URLSearchParams(window.location.search);
  return parseUrlState(searchParams);
}

/**
 * Generate a shareable URL for the current state
 */
export function generateShareUrl(state: UrlState): string {
  if (typeof window === 'undefined') return '';

  const params = buildUrlParams(state);
  const base = `${window.location.origin}${window.location.pathname}`;

  return params.toString() ? `${base}?${params.toString()}` : base;
}
