// API client for Octohedra backend

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// Types matching backend routers/generate.py

export type LayerShape = 'fractal' | 'solid';
export type PresetType = 'flake' | 'tower' | 'evil_tower' | 'flower' | 'temple_complex';

// New spawn model
export type SpawnDirection = 'out' | 'in' | 'side';

// Legacy types (for backwards compatibility)
export type BranchDirection = 'outwards' | 'inwards' | 'sideways' | 'upwards';
export type BranchStyle = 'waist' | 'edge';

export interface Layer {
  depth: number;
  shape?: LayerShape;

  // New spawn model
  spawn?: SpawnDirection[];
  bloom?: boolean;  // Do spawns continue branching?
  echo?: boolean;   // Do spawns contain full recipe at smaller scale?

  // Legacy (for backwards compatibility)
  branch_directions?: BranchDirection[];
  branch_style?: BranchStyle;
}

export interface Recipe {
  preset?: PresetType;
  layers: Layer[];
  six_way?: boolean;
  grid_depth?: number;
  grid_min_depth?: number;
}

export interface GenerateParams {
  layers?: Layer[];
  preset?: PresetType;
  depth?: number;
  stack_height?: number;
  six_way?: boolean;
  grid_depth?: number;
  grid_min_depth?: number;
  config?: string;
}

// Preset options for the UI
export const PRESETS: { value: PresetType; label: string }[] = [
  { value: 'flake', label: 'Flake' },
  { value: 'tower', label: 'Tower' },
  { value: 'evil_tower', label: 'Evil Tower' },
  { value: 'flower', label: 'Flower' },
  { value: 'temple_complex', label: 'Temple Complex' },
];

// Layer shape options for the recipe builder
export const LAYER_SHAPE_OPTIONS: { value: LayerShape; label: string; description: string }[] = [
  { value: 'fractal', label: 'Fractal', description: 'Branch in all 6 directions - classic fractal' },
  { value: 'solid', label: 'Solid', description: 'Fill solid with no fractal recursion' },
];

// Spawn direction options for the recipe builder
export const SPAWN_DIRECTION_OPTIONS: { value: SpawnDirection; label: string; description: string }[] = [
  { value: 'out', label: 'Out', description: 'Away from parent direction' },
  { value: 'in', label: 'In', description: 'Back toward parent' },
  { value: 'side', label: 'Side', description: 'Perpendicular to parent' },
];

// Legacy: Branch direction options (for backwards compatibility)
export const BRANCH_DIRECTION_OPTIONS: { value: BranchDirection; label: string; description: string }[] = [
  { value: 'upwards', label: 'Up', description: 'Continue building central stack (+z)' },
  { value: 'outwards', label: 'Out', description: 'Away from parent direction' },
  { value: 'inwards', label: 'In', description: 'Back toward parent' },
  { value: 'sideways', label: 'Side', description: 'Perpendicular to parent' },
];

// Legacy: Branch style options (for backwards compatibility)
export const BRANCH_STYLE_OPTIONS: { value: BranchStyle; label: string; description: string }[] = [
  { value: 'waist', label: 'Waist', description: 'Sub-towers at narrower point (simple, no recursion)' },
  { value: 'edge', label: 'Edge', description: 'Sub-towers at outer extent (recursive)' },
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
  recipe: { layers: Layer[]; six_way?: boolean; grid_depth?: number; grid_min_depth?: number },
  configName: string = 'print_medium'
): Promise<Blob> {
  const response = await fetch(`${API_BASE}/api/v1/generate/stl`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      layers: recipe.layers,
      six_way: recipe.six_way,
      grid_depth: recipe.grid_depth,
      grid_min_depth: recipe.grid_min_depth,
      config: configName,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`STL generation failed: ${text}`);
  }

  return response.blob();
}

// Shape storage types
export interface StoredShape {
  id: string;
  layers: Layer[];
  sixWay: boolean;
  stlUrl: string;
  screenshotUrl: string;
  createdAt: string;
}

/**
 * Save a shape with screenshot to Vercel Blob storage
 */
export async function saveShape(
  layers: Layer[],
  sixWay: boolean,
  screenshot: Blob,
  stl?: Blob
): Promise<StoredShape> {
  const formData = new FormData();
  formData.append('layers', JSON.stringify(layers));
  formData.append('sixWay', String(sixWay));
  formData.append('screenshot', screenshot, 'screenshot.png');
  if (stl) {
    formData.append('stl', stl, 'model.stl');
  }

  const response = await fetch('/api/shapes', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Failed to save shape: ${text}`);
  }

  return response.json();
}

/**
 * Get a stored shape by ID
 */
export async function getShape(id: string): Promise<StoredShape | null> {
  try {
    const response = await fetch(`/api/shapes/${id}`);

    // 404 = shape doesn't exist, 503 = blob not configured
    if (response.status === 404 || response.status === 503) {
      return null;
    }

    if (!response.ok) {
      return null;
    }

    return response.json();
  } catch {
    return null;
  }
}

/**
 * List recent shapes
 */
export async function listRecentShapes(limit: number = 10): Promise<StoredShape[]> {
  try {
    const response = await fetch(`/api/shapes?limit=${limit}`);

    // 503 = blob not configured
    if (!response.ok) {
      return [];
    }

    return response.json();
  } catch {
    return [];
  }
}
