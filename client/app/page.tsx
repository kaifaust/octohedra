'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { RotateCw, PanelLeftClose, PanelLeftOpen, Download } from 'lucide-react';
import { FractalViewer } from '@/components/FractalViewer';
import { RecipeBuilder } from '@/components/RecipeBuilder';
import { useFractalGeneration } from '@/hooks/useFractalGeneration';
import { PresetType, Layer, PRESETS, downloadStl, PrintConfig, PRINT_CONFIG_OPTIONS } from '@/lib/api';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Toggle } from '@/components/ui/toggle';
import { Label } from '@/components/ui/label';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

export default function Home() {
  // Current preset (for the selector)
  const [selectedPreset, setSelectedPreset] = useState<PresetType>('flake');

  // Recipe state (layers + six_way)
  const [layers, setLayers] = useState<Layer[]>([{ depth: 2 }]);
  const [sixWay, setSixWay] = useState(false);

  // Track if recipe has been modified from preset
  const [isModified, setIsModified] = useState(false);

  // Camera animation toggle
  const [autoRotate, setAutoRotate] = useState(false);

  // Drawer visibility
  const [drawerOpen, setDrawerOpen] = useState(true);

  const { objData, fileSize, isLoading, error, generate, fetchPresetRecipe } = useFractalGeneration();

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
      setSixWay(recipe.six_way || false);
      setIsModified(false);
    }
  }, [fetchPresetRecipe]);

  // Generate default fractal on page load
  useEffect(() => {
    fetchPresetRecipe('flake').then((recipe) => {
      if (recipe) {
        setLayers(recipe.layers);
        setSixWay(recipe.six_way || false);
        generate({
          layers: recipe.layers,
          six_way: recipe.six_way,
        });
      }
    });
  }, [generate, fetchPresetRecipe]);

  // Handle preset selection - load and generate immediately
  const handlePresetSelect = useCallback(async (preset: PresetType) => {
    setSelectedPreset(preset);
    const recipe = await fetchPresetRecipe(preset);
    if (recipe) {
      setLayers(recipe.layers);
      setSixWay(recipe.six_way || false);
      setIsModified(false);
      // Generate immediately with the loaded recipe
      generate({
        layers: recipe.layers,
        six_way: recipe.six_way,
      });
    }
  }, [fetchPresetRecipe, generate]);

  // Handle recipe changes (mark as modified and auto-generate)
  const handleLayersChange = useCallback((newLayers: Layer[]) => {
    setLayers(newLayers);
    setIsModified(true);
  }, []);

  // Track if initial load is done
  const initialLoadDone = useRef(false);

  // Auto-generate when recipe changes (debounced)
  useEffect(() => {
    // Skip auto-generation during initial load
    if (!initialLoadDone.current) return;

    const timer = setTimeout(() => {
      generate({
        layers,
        six_way: sixWay,
      });
    }, 300); // 300ms debounce

    return () => clearTimeout(timer);
  }, [layers, sixWay, generate]);

  // Mark initial load as done after first generation
  useEffect(() => {
    if (objData && !initialLoadDone.current) {
      initialLoadDone.current = true;
    }
  }, [objData]);

  // Calculate total depth for zoom (sum of all layer depths)
  const totalDepth = layers.reduce((sum, l) => sum + l.depth, 0);

  return (
    <main className="relative w-full h-dvh overflow-hidden">
      <FractalViewer objData={objData} totalDepth={totalDepth} autoRotate={autoRotate} onAutoRotateChange={setAutoRotate} />

      {/* Centered loading spinner */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="h-12 w-12 border-4 border-white/30 border-t-white rounded-full animate-spin" />
        </div>
      )}

      {/* Collapsed drawer toggle button */}
      {!drawerOpen && (
        <Button
          variant="secondary"
          size="icon"
          className="absolute top-4 left-4 bg-card/80 backdrop-blur-sm border-border/50"
          onClick={() => setDrawerOpen(true)}
          aria-label="Open panel"
        >
          <PanelLeftOpen className="h-4 w-4" />
        </Button>
      )}

      {/* Drawer panel */}
      {drawerOpen && (
        <Card className="absolute top-4 left-4 w-96 max-h-[calc(100dvh-2rem)] flex flex-col border-border/50 bg-card/80 backdrop-blur-sm pb-0">
          <CardHeader className="pb-2 shrink-0">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="icon-sm"
                  onClick={() => setDrawerOpen(false)}
                  aria-label="Close panel"
                  className="h-6 w-6 text-muted-foreground hover:text-foreground"
                >
                  <PanelLeftClose className="h-4 w-4" />
                </Button>
                <CardTitle className="text-xl">Octoflake</CardTitle>
              </div>
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

          <CardContent className="overflow-y-auto flex-1 min-h-0 pt-0 pb-4">
            <div className="space-y-4">
              {/* Preset selector */}
              <div className="space-y-2">
                <Label>Start from Preset</Label>
                <div className="grid grid-cols-2 gap-1">
                  {PRESETS.map((preset) => (
                    <Button
                      key={preset.value}
                      variant={selectedPreset === preset.value && !isModified ? 'default' : 'secondary'}
                      size="sm"
                      onClick={() => handlePresetSelect(preset.value)}
                      className="w-full text-xs"
                    >
                      {preset.label}
                    </Button>
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
                onLayersChange={handleLayersChange}
              />

              {/* Error display */}
              {error && (
                <p className="text-destructive text-xs bg-destructive/10 p-2 rounded-md">
                  {error.message}
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* File size display and download button */}
      {fileSize && (
        <div className="absolute bottom-4 right-4 flex items-center gap-2 text-xs text-white/70 bg-black/30 px-2 py-1 rounded backdrop-blur-sm">
          <span>{fileSize}</span>
          {objData && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button
                  className="hover:text-white transition-colors"
                  title="Download STL"
                >
                  <Download className="h-3 w-3" />
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" side="top">
                <DropdownMenuLabel>Download STL</DropdownMenuLabel>
                <DropdownMenuSeparator />
                {PRINT_CONFIG_OPTIONS.map((config) => (
                  <DropdownMenuItem
                    key={config.value}
                    onClick={async () => {
                      try {
                        const blob = await downloadStl({ layers, six_way: sixWay }, config.value);
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `octoflake-${config.value}.stl`;
                        a.click();
                        URL.revokeObjectURL(url);
                      } catch (e) {
                        console.error('STL download failed:', e);
                      }
                    }}
                  >
                    <div className="flex flex-col">
                      <span className="font-medium">{config.label}</span>
                      <span className="text-xs text-muted-foreground">{config.description}</span>
                    </div>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      )}
    </main>
  );
}
