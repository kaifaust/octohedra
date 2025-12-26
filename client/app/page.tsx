'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { RotateCw, PanelLeftClose, PanelLeftOpen, Download, Info, Share2, Check } from 'lucide-react';
import { FractalViewer, FractalViewerHandle } from '@/components/FractalViewer';
import { RecipeBuilder } from '@/components/RecipeBuilder';
import { MobileBottomSheet } from '@/components/MobileBottomSheet';
import { RecentShapesPanel, RecentShapesPanelHandle } from '@/components/RecentShapesPanel';
import { useFractalGeneration } from '@/hooks/useFractalGeneration';
import { encodeLayers, decodeLayers } from '@/hooks/useUrlSync';
import { PresetType, Layer, PRESETS, downloadStl, PRINT_CONFIG_OPTIONS, saveShape, getShape } from '@/lib/api';
import { generateShapeId } from '@/lib/shapes';
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

// Recipe state combines layers + sixWay for atomic updates
interface RecipeState {
  layers: Layer[];
  sixWay: boolean;
}

export interface HomeClientProps {
  initialRecipe?: string; // encoded recipe from URL path (e.g., "3f.d-3f" or "3f.d-3f-6")
}

export function HomeClient({ initialRecipe }: HomeClientProps) {
  const router = useRouter();

  // Initialization: false until first load completes
  const [isInitialized, setIsInitialized] = useState(false);

  // Recipe state - null until initialized
  const [recipe, setRecipe] = useState<RecipeState | null>(null);

  // Generation version - increments on every intentional recipe change
  // The generate effect only runs when this changes, preventing duplicates
  const [generationVersion, setGenerationVersion] = useState(0);

  // UI state
  const [selectedPreset, setSelectedPreset] = useState<PresetType | null>(null);
  const [isModified, setIsModified] = useState(false);
  const [autoRotate, setAutoRotate] = useState(true);
  // Start closed to avoid hydration mismatch, open on desktop after mount
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [shareTooltip, setShareTooltip] = useState<'idle' | 'copied'>('idle');

  // Shape saving state
  const [currentShapeId, setCurrentShapeId] = useState<string | null>(null);
  const [recentPanelOpen, setRecentPanelOpen] = useState(true);
  const [skipSaveForShape, setSkipSaveForShape] = useState<string | null>(null);
  // Skip saving until user makes an intentional change (not initial load)
  const [saveEnabled, setSaveEnabled] = useState(false);
  // Thumbnail URL for showing preview while model loads
  const [thumbnailUrl, setThumbnailUrl] = useState<string | null>(null);
  // Track if the 3D model has finished rendering (separate from API loading)
  const [modelReady, setModelReady] = useState(false);
  const viewerRef = useRef<FractalViewerHandle>(null);
  const recentShapesPanelRef = useRef<RecentShapesPanelHandle>(null);

  const { objData, fileSize, isLoading, error, generate, fetchPresetRecipe } = useFractalGeneration();

  // Sync recipe state to URL path
  useEffect(() => {
    if (!isInitialized || !recipe) return;

    const layersEncoded = encodeLayers(recipe.layers);
    const sixWaySuffix = recipe.sixWay ? '-6' : '';
    const newPath = `/r/${layersEncoded}${sixWaySuffix}`;

    // Only update if path changed
    if (window.location.pathname !== newPath) {
      router.replace(newPath, { scroll: false });
    }
  }, [recipe, isInitialized, router]);

  // Set viewport height CSS variable for mobile compatibility
  useEffect(() => {
    const setVH = () => {
      document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
    };
    setVH();
    window.addEventListener('resize', setVH);
    return () => window.removeEventListener('resize', setVH);
  }, []);

  // Open drawer by default on desktop (after hydration to avoid mismatch)
  useEffect(() => {
    const mediaQuery = window.matchMedia('(min-width: 768px)');
    if (mediaQuery.matches) {
      // Use event handler pattern to satisfy lint rule
      const handler = () => setDrawerOpen(true);
      handler();
    }
  }, []);

  // Initialize from initialRecipe prop or default preset (runs once on mount)
  useEffect(() => {
    if (isInitialized) return;

    const initialize = async () => {
      // If we have an initial recipe from the URL path, use it
      if (initialRecipe) {
        const hasSixWay = initialRecipe.endsWith('-6');
        const layersParam = hasSixWay ? initialRecipe.slice(0, -2) : initialRecipe;
        const layers = decodeLayers(layersParam);

        if (layers && layers.length > 0) {
          setRecipe({
            layers,
            sixWay: hasSixWay,
          });
          setIsModified(true);
          setSelectedPreset(null);
          setGenerationVersion(1);
          setSaveEnabled(true);
          setIsInitialized(true);
          return;
        }
      }

      // Default: load flake preset
      const defaultRecipe = await fetchPresetRecipe('flake');
      if (defaultRecipe) {
        setRecipe({
          layers: defaultRecipe.layers,
          sixWay: defaultRecipe.six_way ?? false,
        });
        setSelectedPreset('flake');
        setIsModified(false);
        setGenerationVersion(1);
      }

      setIsInitialized(true);
    };

    initialize();
  }, [isInitialized, initialRecipe, fetchPresetRecipe]);

  // Single effect for all generation - triggered by generationVersion changes
  // This is the ONLY place generate() is called, making the flow predictable
  useEffect(() => {
    if (generationVersion === 0 || !recipe) return;

    // Reset model ready state when starting new generation
    setModelReady(false);

    // Update current shape ID for tracking
    const shapeId = generateShapeId(recipe.layers, recipe.sixWay);
    setCurrentShapeId(shapeId);

    // Try to fetch existing shape thumbnail for loading preview
    getShape(shapeId).then((existingShape) => {
      if (existingShape?.screenshotUrl) {
        setThumbnailUrl(existingShape.screenshotUrl);
      } else {
        setThumbnailUrl(null);
      }
    });

    // Debounce for rapid changes (e.g., slider dragging)
    const timer = setTimeout(() => {
      generate({
        layers: recipe.layers,
        six_way: recipe.sixWay,
      });
    }, 300);

    return () => clearTimeout(timer);
  }, [generationVersion, recipe, generate]);

  // Save shape screenshot after generation completes (with delay for render)
  // Use a ref to track saving state to avoid infinite loops
  const savingShapeRef = useRef(false);

  useEffect(() => {
    if (!objData || !recipe || !currentShapeId) return;
    if (savingShapeRef.current) return;

    // Skip save during initial load - only save after user makes changes
    if (!saveEnabled) return;

    // Skip save if this shape was selected from recents (already exists)
    if (skipSaveForShape === currentShapeId) {
      return;
    }

    // Wait for the shape to render before capturing
    const timer = setTimeout(async () => {
      if (savingShapeRef.current) return;

      try {
        savingShapeRef.current = true;

        // Check if shape already exists
        const existingShape = await getShape(currentShapeId);
        if (existingShape) {
          return;
        }

        // Capture screenshot
        const screenshot = await viewerRef.current?.captureScreenshot();
        if (!screenshot) {
          return;
        }

        // Save shape
        await saveShape(recipe.layers, recipe.sixWay, screenshot);

        // Refresh recent shapes panel
        recentShapesPanelRef.current?.refresh();
      } catch (err) {
        console.error('Failed to save shape:', err);
      } finally {
        savingShapeRef.current = false;
      }
    }, 500); // Wait for render

    return () => clearTimeout(timer);
  }, [objData, recipe, currentShapeId, skipSaveForShape, saveEnabled]);

  // Handle selecting a shape from the recent shapes panel
  const handleSelectRecentShape = useCallback((layers: Layer[], sixWay: boolean) => {
    // Mark this shape to skip saving (it already exists in storage)
    const shapeId = generateShapeId(layers, sixWay);
    setSkipSaveForShape(shapeId);

    setRecipe({ layers, sixWay });
    setSelectedPreset(null);
    setIsModified(true);
    setGenerationVersion(v => v + 1);
  }, []);

  // Handle preset selection - just updates state, generation effect handles the rest
  const handlePresetSelect = useCallback(async (preset: PresetType) => {
    setSelectedPreset(preset);
    setSkipSaveForShape(null); // Clear skip flag for new shapes
    setSaveEnabled(true); // Enable saving after user action
    const presetRecipe = await fetchPresetRecipe(preset);
    if (presetRecipe) {
      setRecipe({
        layers: presetRecipe.layers,
        sixWay: presetRecipe.six_way ?? false,
      });
      setIsModified(false);
      setGenerationVersion(v => v + 1);
    }
  }, [fetchPresetRecipe]);

  // Handle layer changes from RecipeBuilder
  const handleLayersChange = useCallback((newLayers: Layer[]) => {
    setRecipe(prev => prev ? { ...prev, layers: newLayers } : null);
    setSkipSaveForShape(null); // Clear skip flag for new shapes
    setSaveEnabled(true); // Enable saving after user action
    setIsModified(true);
    setGenerationVersion(v => v + 1);
  }, []);

  // Handle share button click - copy current URL
  const handleShare = useCallback(async () => {
    if (!recipe) return;

    // Current URL already has the /r/[recipe] format
    const url = window.location.href;

    try {
      await navigator.clipboard.writeText(url);
      setShareTooltip('copied');
      setTimeout(() => setShareTooltip('idle'), 2000);
    } catch {
      // Fallback for browsers without clipboard API
      prompt('Copy this URL to share:', url);
    }
  }, [recipe]);

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
      {recipe && recipe.layers.length > 0 && (
        <RecipeBuilder
          layers={recipe.layers}
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

  // File info bar content - shared between positions
  const fileInfoBar = fileSize && (
    <div className="flex items-center gap-2 text-xs text-white/70 bg-black/30 px-2 py-1 rounded backdrop-blur-sm">
      <span>{fileSize}</span>
      {objData && (
        <DropdownMenu modal={false}>
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
                  if (!recipe) return;
                  try {
                    const blob = await downloadStl(
                      { layers: recipe.layers, six_way: recipe.sixWay },
                      config.value
                    );
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
  );

  return (
    <main className="relative w-full h-dvh overflow-hidden">
      <FractalViewer
        ref={viewerRef}
        objData={objData}
        autoRotate={autoRotate}
        onAutoRotateChange={setAutoRotate}
        thumbnailUrl={thumbnailUrl}
        isLoading={isLoading}
        onModelReady={() => setModelReady(true)}
      />

      {/* Centered loading spinner - show while API is loading OR model is parsing/rendering */}
      {(isLoading || !modelReady) && (
        <div className="absolute inset-0 z-2 flex items-center justify-center pointer-events-none">
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
          onOpenChange={(open) => {
            setDrawerOpen(open);
            // Close recent panel when opening control panel on mobile
            if (open) {
              setRecentPanelOpen(false);
            }
          }}
          title="Octohedra"
          headerActions={headerActions}
        >
          {controlPanelContent}
        </MobileBottomSheet>
      </div>

      {/* File size display, download button, and credits */}
      {/* Mobile: top-right, Desktop: bottom-right */}
      <div className="absolute top-4 right-4 md:top-auto md:bottom-4">
        {fileInfoBar}
      </div>

      {/* Recent shapes panel - right side */}
      <RecentShapesPanel
        ref={recentShapesPanelRef}
        onSelectShape={handleSelectRecentShape}
        isOpen={recentPanelOpen}
        onOpenChange={(open) => {
          setRecentPanelOpen(open);
          // On mobile, close the control panel when opening recent panel
          if (open && window.innerWidth < 768) {
            setDrawerOpen(false);
          }
        }}
      />
    </main>
  );
}

// Default export for the home page - no initial recipe, will load default preset
export default function Home() {
  return <HomeClient />;
}
