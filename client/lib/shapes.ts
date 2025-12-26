import { Layer } from './api';

/**
 * Stored shape metadata
 */
export interface StoredShape {
  id: string;
  layers: Layer[];
  sixWay: boolean;
  stlUrl: string;
  screenshotUrl: string;
  createdAt: string; // ISO date string
}

/**
 * Generate a deterministic ID from recipe parameters
 * This allows deduplication - same recipe = same ID
 */
export function generateShapeId(layers: Layer[], sixWay: boolean): string {
  const normalized = JSON.stringify({ layers, sixWay });
  // Simple hash function for deterministic IDs
  let hash = 0;
  for (let i = 0; i < normalized.length; i++) {
    const char = normalized.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  // Convert to positive hex string
  return Math.abs(hash).toString(16).padStart(8, '0');
}

/**
 * Encode recipe to base64 for storage in blob pathname
 */
export function encodeRecipe(layers: Layer[], sixWay: boolean): string {
  const data = JSON.stringify({ layers, sixWay });
  // Use base64url encoding (no +, /, or = which could cause path issues)
  return Buffer.from(data).toString('base64url');
}

/**
 * Decode recipe from base64 blob pathname
 */
export function decodeRecipe(encoded: string): { layers: Layer[]; sixWay: boolean } | null {
  try {
    const data = Buffer.from(encoded, 'base64url').toString('utf-8');
    return JSON.parse(data);
  } catch {
    return null;
  }
}
