/**
 * Recipe encoding/decoding utilities
 * These are pure functions that work on both server and client
 */

import { Layer, LayerShape, SpawnDirection } from '@/lib/api';

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
 * Parse a recipe string from URL path format
 * Format: "3f.d-3f" or "3f.d-3f-6" (with sixWay suffix)
 */
export function parseRecipeFromPath(recipe: string): { layers: Layer[]; sixWay: boolean } | null {
  const hasSixWay = recipe.endsWith('-6');
  const layersParam = hasSixWay ? recipe.slice(0, -2) : recipe;
  const layers = decodeLayers(layersParam);

  if (!layers) return null;

  return { layers, sixWay: hasSixWay };
}

/**
 * Encode recipe to URL path format
 */
export function encodeRecipeToPath(layers: Layer[], sixWay: boolean): string {
  const layersEncoded = encodeLayers(layers);
  const sixWaySuffix = sixWay ? '-6' : '';
  return `${layersEncoded}${sixWaySuffix}`;
}
