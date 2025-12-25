'use client';

import { useState, useEffect, useCallback, useMemo } from 'react';
import { RotateCw, PanelLeftClose, PanelLeftOpen, Download, Info, Share2, Check } from 'lucide-react';
import { FractalViewer } from '@/components/FractalViewer';
import { RecipeBuilder } from '@/components/RecipeBuilder';
import { MobileBottomSheet } from '@/components/MobileBottomSheet';
import { useFractalGeneration } from '@/hooks/useFractalGeneration';
import { useUrlSync, getInitialUrlState, generateShareUrl, UrlState } from '@/hooks/useUrlSync';
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
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';

type InitState = 'pending' | 'loading' | 'ready';

export default function Home() {
  // Initialization state machine - cleaner than ref-based tracking
  const [initState, setInitState] = useState<InitState>('pending');

  // Recipe state (layers + six_way)
  const [layers, setLayers] = useState<Layer[] | null>(null);
  const [sixWay, setSixWay] = useState(false);

  // UI state
  const [selectedPreset, setSelectedPreset] = useState<PresetType | null>(null);
  const [isModified, setIsModified] = useState(false);
  const [autoRotate, setAutoRotate] = useState(true);
  const [drawerOpen, setDrawerOpen] = useState(true);
  const [shareTooltip, setShareTooltip] = useState<'idle' | 'copied'>('idle');

  const { objData, fileSize, isLoading, error, generate, fetchPresetRecipe } = useFractalGeneration();

  // Memoize URL state to prevent unnecessary re-renders
  const urlState = useMemo<UrlState>(() => ({
    layers: layers ?? undefined,
    sixWay,
    autoRotate,
  }), [layers, sixWay, autoRotate]);

  // Sync state to URL (only after initialization)
  useUrlSync(urlState, initState === 'ready');

  // Set viewport height CSS variable for mobile compatibility
  useEffect(() => {
    const setVH = () => {
      document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
    };
    setVH();
    window.addEventListener('resize', setVH);
    return () => window.removeEventListener('resize', setVH);
  }, []);

  // Initialize from URL params or default preset
  useEffect(() => {
    if (initState !== 'pending') return;

    setInitState('loading');

    const initializeFromUrl = async () => {
      const urlParams = getInitialUrlState();

      // If URL has layers, use them directly
      if (urlParams.layers && urlParams.layers.length > 0) {
        setLayers(urlParams.layers);
        setSixWay(urlParams.sixWay ?? false);
        setAutoRotate(urlParams.autoRotate ?? true);
        setIsModified(true); // URL params are considered "modified" from any preset
        setSelectedPreset(null);

        // Generate with URL layers
        await generate({
          layers: urlParams.layers,
          six_way: urlParams.sixWay ?? false,
        });

        setInitState('ready');
        return;
      }

      // If URL has preset, load it
      if (urlParams.preset) {
        const recipe = await fetchPresetRecipe(urlParams.preset);
        if (recipe) {
          setLayers(recipe.layers);
          setSixWay(recipe.six_way ?? false);
          setAutoRotate(urlParams.autoRotate ?? true);
          setSelectedPreset(urlParams.preset);
          setIsModified(false);

          await generate({
            layers: recipe.layers,
            six_way: recipe.six_way,
          });

          setInitState('ready');
          return;
        }
      }

      // Default: load flake preset
      const recipe = await fetchPresetRecipe('flake');
      if (recipe) {
        setLayers(recipe.layers);
        setSixWay(recipe.six_way ?? false);
        setSelectedPreset('flake');
        setIsModified(false);

        await generate({
          layers: recipe.layers,
          six_way: recipe.six_way,
        });
      }

      setInitState('ready');
    };

    initializeFromUrl();
  }, [initState, generate, fetchPresetRecipe]);

  // Handle preset selection
  const handlePresetSelect = useCallback(async (preset: PresetType) => {
    setSelectedPreset(preset);
    const recipe = await fetchPresetRecipe(preset);
    if (recipe) {
      setLayers(recipe.layers);
      setSixWay(recipe.six_way ?? false);
      setIsModified(false);
      generate({
        layers: recipe.layers,
        six_way: recipe.six_way,
      });
    }
  }, [fetchPresetRecipe, generate]);

  // Handle layer changes from RecipeBuilder
  const handleLayersChange = useCallback((newLayers: Layer[]) => {
    setLayers(newLayers);
    setIsModified(true);
  }, []);

  // Auto-generate when recipe changes (after initialization)
  useEffect(() => {
    if (initState !== 'ready' || !layers) return;

    const timer = setTimeout(() => {
      generate({
        layers,
        six_way: sixWay,
      });
    }, 300);

    return () => clearTimeout(timer);
  }, [layers, sixWay, generate, initState]);

  // Handle share button click
  const handleShare = useCallback(async () => {
    if (!layers) return;

    const url = generateShareUrl({ layers, sixWay, autoRotate });

    try {
      await navigator.clipboard.writeText(url);
      setShareTooltip('copied');
      setTimeout(() => setShareTooltip('idle'), 2000);
    } catch {
      // Fallback for browsers without clipboard API
      prompt('Copy this URL to share:', url);
    }
  }, [layers, sixWay, autoRotate]);

  // Control panel content - shared between desktop and mobile
  const controlPanelContent = (
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
  );

  // Header actions - shared between desktop and mobile
  const headerActions = (
    <div className="flex items-center gap-1">
      <Toggle
        pressed={autoRotate}
        onPressedChange={setAutoRotate}
        size="sm"
        aria-label="Toggle animation"
      >
        <RotateCw className={`h-4 w-4 ${autoRotate ? 'animate-spin' : ''}`} />
        <span className="ml-1 hidden sm:inline">{autoRotate ? 'Animating' : 'Animate'}</span>
      </Toggle>
      <Tooltip open={shareTooltip === 'copied' ? true : undefined}>
        <TooltipTrigger asChild>
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              handleShare();
            }}
            className="text-muted-foreground hover:text-foreground"
            aria-label="Share configuration"
          >
            {shareTooltip === 'copied' ? (
              <Check className="h-4 w-4 text-green-500" />
            ) : (
              <Share2 className="h-4 w-4" />
            )}
          </Button>
        </TooltipTrigger>
        <TooltipContent>
          {shareTooltip === 'copied' ? 'Copied!' : 'Copy share link'}
        </TooltipContent>
      </Tooltip>
    </div>
  );

  return (
    <main className="relative w-full h-dvh overflow-hidden">
      <FractalViewer objData={objData} autoRotate={autoRotate} onAutoRotateChange={setAutoRotate} />

      {/* Centered loading spinner */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="h-12 w-12 border-4 border-white/30 border-t-white rounded-full animate-spin" />
        </div>
      )}

      {/* Desktop: Side drawer panel - hidden on mobile via CSS */}
      <div className="hidden md:block">
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
              {headerActions}
            </div>

            {/* Content */}
            <div className="overflow-y-auto flex-1 min-h-0 px-4 pb-4">
              {controlPanelContent}
            </div>
          </div>
        )}
      </div>

      {/* Mobile: Bottom sheet - hidden on desktop via CSS */}
      <div className="md:hidden">
        <MobileBottomSheet
          isOpen={drawerOpen}
          onOpenChange={setDrawerOpen}
          title="Octohedra"
          headerActions={headerActions}
        >
          {controlPanelContent}
        </MobileBottomSheet>
      </div>

      {/* File size display, download button, and credits */}
      {fileSize && (
        <div className="absolute bottom-4 md:bottom-4 right-4 flex items-center gap-2 text-xs text-white/70 bg-black/30 px-2 py-1 rounded backdrop-blur-sm z-50">
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
              <DropdownMenuContent align="end" side="top" className="z-50">
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
            <DialogContent className="bg-card/95 backdrop-blur-sm border-border/50 z-50">
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
