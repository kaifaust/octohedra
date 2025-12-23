'use client';

import { useState, useEffect, useCallback } from 'react';
import { FractalViewer } from '@/components/FractalViewer';
import { RecipeBuilder } from '@/components/RecipeBuilder';
import { useFractalGeneration } from '@/hooks/useFractalGeneration';
import { PresetType, Layer, DepthRule, PRESETS } from '@/lib/api';

export default function Home() {
  // Current preset (for the selector)
  const [selectedPreset, setSelectedPreset] = useState<PresetType>('flake');

  // Recipe state (layers + depth rules)
  const [layers, setLayers] = useState<Layer[]>([{ depth: 2, fill_depth: 0 }]);
  const [depthRules, setDepthRules] = useState<DepthRule[]>([]);

  // Track if recipe has been modified from preset
  const [isModified, setIsModified] = useState(false);

  const { objData, isLoading, error, generate, fetchPresetRecipe } = useFractalGeneration();

  // Set viewport height CSS variable for mobile compatibility
  useEffect(() => {
    const setVH = () => {
      document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
    };
    setVH();
    window.addEventListener('resize', setVH);
    return () => window.removeEventListener('resize', setVH);
  }, []);

  // Load preset recipe when preset changes
  const loadPreset = useCallback(async (preset: PresetType) => {
    const recipe = await fetchPresetRecipe(preset);
    if (recipe) {
      setLayers(recipe.layers);
      setDepthRules(recipe.depth_rules);
      setIsModified(false);
    }
  }, [fetchPresetRecipe]);

  // Generate default fractal on page load
  useEffect(() => {
    loadPreset('flake').then(() => {
      generate({
        preset: 'flake',
        depth: 2,
      });
    });
  }, [generate, loadPreset]);

  // Handle preset selection
  const handlePresetSelect = useCallback(async (preset: PresetType) => {
    setSelectedPreset(preset);
    await loadPreset(preset);
  }, [loadPreset]);

  // Handle recipe changes (mark as modified)
  const handleLayersChange = useCallback((newLayers: Layer[]) => {
    setLayers(newLayers);
    setIsModified(true);
  }, []);

  const handleDepthRulesChange = useCallback((newRules: DepthRule[]) => {
    setDepthRules(newRules);
    setIsModified(true);
  }, []);

  // Handle generate
  const handleGenerate = useCallback(() => {
    generate({
      layers,
      depth_rules: depthRules,
    });
  }, [generate, layers, depthRules]);

  // Calculate max depth for viewer
  const maxDepth = Math.max(...layers.map(l => l.depth), 1);

  return (
    <main className="relative w-full h-dvh overflow-hidden">
      <FractalViewer objData={objData} depth={maxDepth} />

      <div className="absolute top-4 left-4 w-80 max-h-[calc(100dvh-2rem)] overflow-y-auto p-4 bg-gray-900/80 backdrop-blur-sm rounded-lg text-white space-y-4">
        <h1 className="text-xl font-bold">Octoflake</h1>

        {/* Preset selector */}
        <div>
          <label className="block text-sm font-medium mb-2">Start from Preset</label>
          <div className="grid grid-cols-2 gap-1">
            {PRESETS.map((preset) => (
              <button
                key={preset.value}
                onClick={() => handlePresetSelect(preset.value)}
                className={`px-2 py-1.5 text-xs rounded transition-colors ${
                  selectedPreset === preset.value && !isModified
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 hover:bg-gray-600 text-gray-200'
                }`}
                title={preset.description}
              >
                {preset.label}
              </button>
            ))}
          </div>
          {isModified && (
            <p className="text-xs text-purple-400 mt-1">Recipe modified from preset</p>
          )}
        </div>

        {/* Divider */}
        <div className="border-t border-gray-700" />

        {/* Recipe builder */}
        <RecipeBuilder
          layers={layers}
          depthRules={depthRules}
          onLayersChange={handleLayersChange}
          onDepthRulesChange={handleDepthRulesChange}
        />

        {/* Generate button */}
        <button
          onClick={handleGenerate}
          disabled={isLoading}
          className="w-full py-2 rounded font-semibold transition-colors bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Generating...' : 'Generate'}
        </button>

        {/* Error display */}
        {error && (
          <p className="text-red-400 text-xs bg-red-900/30 p-2 rounded">
            {error.message}
          </p>
        )}

        {/* Success indicator */}
        {objData && (
          <p className="text-green-400 text-xs">
            {Math.round(objData.length / 1024)}KB loaded
          </p>
        )}
      </div>
    </main>
  );
}
