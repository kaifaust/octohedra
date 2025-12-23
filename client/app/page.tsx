'use client';

import { useState, useEffect, useCallback } from 'react';
import { RotateCw } from 'lucide-react';
import { FractalViewer } from '@/components/FractalViewer';
import { RecipeBuilder } from '@/components/RecipeBuilder';
import { useFractalGeneration } from '@/hooks/useFractalGeneration';
import { PresetType, Layer, DepthRule, PRESETS } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Toggle } from '@/components/ui/toggle';
import { Label } from '@/components/ui/label';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

export default function Home() {
  // Current preset (for the selector)
  const [selectedPreset, setSelectedPreset] = useState<PresetType>('flake');

  // Recipe state (layers + depth rules)
  const [layers, setLayers] = useState<Layer[]>([{ depth: 2, fill_depth: 0 }]);
  const [depthRules, setDepthRules] = useState<DepthRule[]>([]);

  // Track if recipe has been modified from preset
  const [isModified, setIsModified] = useState(false);

  // Camera animation toggle
  const [autoRotate, setAutoRotate] = useState(false);

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
      <FractalViewer objData={objData} depth={maxDepth} autoRotate={autoRotate} />

      <Card className="absolute top-4 left-4 w-96 max-h-[calc(100dvh-2rem)] overflow-y-auto border-border/50 bg-card/80 backdrop-blur-sm">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-xl">Octoflake</CardTitle>
            <Toggle
              pressed={autoRotate}
              onPressedChange={setAutoRotate}
              size="sm"
              aria-label="Toggle animation"
            >
              <RotateCw className={`h-4 w-4 ${autoRotate ? 'animate-spin' : ''}`} />
              <span className="ml-1">{autoRotate ? 'Animating' : 'Animate'}</span>
            </Toggle>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Preset selector */}
          <div className="space-y-2">
            <Label>Start from Preset</Label>
            <div className="grid grid-cols-2 gap-1">
              {PRESETS.map((preset) => (
                <Tooltip key={preset.value}>
                  <TooltipTrigger asChild>
                    <Button
                      variant={selectedPreset === preset.value && !isModified ? 'default' : 'secondary'}
                      size="sm"
                      onClick={() => handlePresetSelect(preset.value)}
                      className="w-full text-xs"
                    >
                      {preset.label}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{preset.description}</p>
                  </TooltipContent>
                </Tooltip>
              ))}
            </div>
            {isModified && (
              <p className="text-xs text-primary">Recipe modified from preset</p>
            )}
          </div>

          <Separator />

          {/* Recipe builder */}
          <RecipeBuilder
            layers={layers}
            depthRules={depthRules}
            onLayersChange={handleLayersChange}
            onDepthRulesChange={handleDepthRulesChange}
          />

          {/* Generate button */}
          <Button
            onClick={handleGenerate}
            disabled={isLoading}
            className="w-full"
            size="lg"
          >
            {isLoading ? 'Generating...' : 'Generate'}
          </Button>

          {/* Error display */}
          {error && (
            <p className="text-destructive text-xs bg-destructive/10 p-2 rounded-md">
              {error.message}
            </p>
          )}

          {/* Success indicator */}
          {objData && (
            <p className="text-muted-foreground text-xs">
              {Math.round(objData.length / 1024)}KB loaded
            </p>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
