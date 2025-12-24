// API client for Octohedra backend

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// Types matching backend routers/generate.py

export type LayerShape = 'fractal' | 'solid';
export type PresetType = 'flake' | 'tower' | 'evil_tower' | 'flower';
export type BranchDirection = 'outwards' | 'inwards' | 'sideways' | 'upwards';

export interface Layer {
  depth: number;
  shape?: LayerShape;
  attach_next_at?: number;
  branch_directions?: BranchDirection[];
}

export interface Recipe {
  preset?: PresetType;
  layers: Layer[];
  six_way?: boolean;
}

export interface GenerateParams {
  layers?: Layer[];
  preset?: PresetType;
  depth?: number;
  stack_height?: number;
  six_way?: boolean;
  config?: string;
}

// Preset options for the UI
export const PRESETS: { value: PresetType; label: string }[] = [
  { value: 'flake', label: 'Flake' },
  { value: 'tower', label: 'Tower' },
  { value: 'evil_tower', label: 'Evil Tower' },
  { value: 'flower', label: 'Flower' },
];

// Layer shape options for the recipe builder
export const LAYER_SHAPE_OPTIONS: { value: LayerShape; label: string; description: string }[] = [
  { value: 'fractal', label: 'Fractal', description: 'Branch in all 6 directions - classic fractal' },
  { value: 'solid', label: 'Solid', description: 'Fill solid with no fractal recursion' },
];

// Branch direction options for the recipe builder
export const BRANCH_DIRECTION_OPTIONS: { value: BranchDirection; label: string; description: string }[] = [
  { value: 'upwards', label: 'Up', description: 'Continue building central stack (+z)' },
  { value: 'outwards', label: 'Out', description: 'Away from parent direction' },
  { value: 'inwards', label: 'In', description: 'Back toward parent' },
  { value: 'sideways', label: 'Side', description: 'Perpendicular to parent' },
];

// Print config options for STL export
export const PRINT_CONFIG_OPTIONS: { value: string; label: string; description: string }[] = [
  { value: 'print_low', label: 'Low', description: 'Fast print, lower detail' },
  { value: 'print_medium', label: 'Medium', description: 'Balanced quality and speed' },
  { value: 'print_high', label: 'High', description: 'High detail, longer print' },
];

/**
 * Generate a fractal mesh (OBJ format)
 */
export async function generateFractal(params: GenerateParams): Promise<string> {
  const response = await fetch(`${API_BASE}/api/v1/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Generation failed: ${text}`);
  }

  return response.text();
}

/**
 * Get the recipe for a preset
 */
export async function getPresetRecipe(
  preset: PresetType,
  depth: number = 3,
  stackHeight: number = 1
): Promise<Recipe> {
  const response = await fetch(
    `${API_BASE}/api/v1/presets/${preset}?depth=${depth}&stack_height=${stackHeight}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch preset: ${preset}`);
  }

  return response.json();
}

/**
 * Download STL file for 3D printing
 */
export async function downloadStl(
  recipe: { layers: Layer[]; six_way?: boolean },
  configName: string = 'print_medium'
): Promise<Blob> {
  const response = await fetch(`${API_BASE}/api/v1/generate/stl`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      layers: recipe.layers,
      six_way: recipe.six_way,
      config: configName,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`STL generation failed: ${text}`);
  }

  return response.blob();
}
