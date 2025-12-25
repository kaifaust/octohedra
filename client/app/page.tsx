'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { RotateCw, PanelLeftClose, PanelLeftOpen, Download, Info } from 'lucide-react';
import { FractalViewer } from '@/components/FractalViewer';
import { RecipeBuilder } from '@/components/RecipeBuilder';
import { useFractalGeneration } from '@/hooks/useFractalGeneration';
import { PresetType, Layer, PRESETS, downloadStl, PRINT_CONFIG_OPTIONS } from '@/lib/api';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Toggle } from '@/components/ui/toggle';
import { Label } from '@/components/ui/label';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

export default function Home() {
  // Current preset (for the selector)
  const [selectedPreset, setSelectedPreset] = useState<PresetType>('flake');

  // Recipe state (layers + six_way) - initialized from preset on load
  const [layers, setLayers] = useState<Layer[] | null>(null);
  const [sixWay, setSixWay] = useState(false);

  // Track if recipe has been modified from preset
  const [isModified, setIsModified] = useState(false);

  // Camera animation toggle
  const [autoRotate, setAutoRotate] = useState(true);

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

  // Handle recipe changes (mark as modified)
  const handleLayersChange = useCallback((newLayers: Layer[]) => {
    setLayers(newLayers);
    setIsModified(true);
  }, []);

  // Track if initial load is done
  const initialLoadDone = useRef(false);

  // Auto-generate when recipe changes (debounced)
  useEffect(() => {
    // Skip auto-generation during initial load or if no layers yet
    if (!initialLoadDone.current || !layers) return;

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

  return (
    <main className="relative w-full h-dvh overflow-hidden">
      <FractalViewer objData={objData} autoRotate={autoRotate} onAutoRotateChange={setAutoRotate} />

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
        <div className="absolute top-4 left-4 max-h-[calc(100dvh-2rem)] flex flex-col rounded-xl border border-border/50 bg-card/80 backdrop-blur-sm shadow-sm">
          {/* Header */}
          <div className="flex items-center gap-4 px-4 py-3">
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
              <h2 className="text-xl font-semibold">Octohedra</h2>
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

          {/* Content */}
          <div className="overflow-y-auto flex-1 min-h-0 px-4 pb-4">
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

              {/* Recipe builder - always shown */}
              {layers && layers.length > 0 && (
                <RecipeBuilder
                  layers={layers}
                  onLayersChange={handleLayersChange}
                />
              )}

              {/* Error display */}
              {error && (
                <p className="text-destructive text-xs bg-destructive/10 p-2 rounded-md">
                  {error.message}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* File size display, download button, and credits */}
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
                      if (!layers) return;
                      try {
                        const blob = await downloadStl({ layers, six_way: sixWay }, config.value);
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `octohedra-${config.value}.stl`;
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
          <span className="mx-1 text-white/30">|</span>
          <Dialog>
            <DialogTrigger asChild>
              <button
                className="hover:text-white transition-colors flex items-center gap-1"
                title="Credits"
              >
                <Info className="h-3 w-3" />
                <span>Credits</span>
              </button>
            </DialogTrigger>
            <DialogContent className="bg-card/95 backdrop-blur-sm border-border/50">
              <DialogHeader>
                <DialogTitle>Credits</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 text-sm">
                <p>
                  Octohedra is an open source fractal geometry generator.
                </p>
                <div className="space-y-2">
                  <div>
                    <span className="font-medium">Jamie</span> - Fractal engine
                  </div>
                  <div>
                    <span className="font-medium">Kai</span> - Web application
                  </div>
                </div>
                <Separator />
                <div>
                  <a
                    href="https://github.com/kaifaust/octohedra"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:underline"
                  >
                    View on GitHub
                  </a>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      )}
    </main>
  );
}
