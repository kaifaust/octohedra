'use client';

import { useCallback } from 'react';
import { Plus, X, ChevronDown, ChevronUp, Copy } from 'lucide-react';
import { Layer, LayerShape, BranchDirection, BranchStyle, LAYER_SHAPE_OPTIONS, BRANCH_DIRECTION_OPTIONS, BRANCH_STYLE_OPTIONS } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

interface RecipeBuilderProps {
  layers: Layer[];
  onLayersChange: (layers: Layer[]) => void;
}

export function RecipeBuilder({
  layers,
  onLayersChange,
}: RecipeBuilderProps) {
  // Update a layer
  const updateLayer = useCallback((index: number, updates: Partial<Layer>) => {
    const newLayers = layers.map((layer, i) =>
      i === index ? { ...layer, ...updates } : layer
    );
    onLayersChange(newLayers);
  }, [layers, onLayersChange]);

  // Add a new layer
  const addLayer = useCallback(() => {
    const lastLayer = layers[layers.length - 1];
    const newDepth = Math.max(1, (lastLayer?.depth || 2) - 1);
    onLayersChange([...layers, { depth: newDepth }]);
  }, [layers, onLayersChange]);

  // Remove a layer
  const removeLayer = useCallback((index: number) => {
    if (layers.length <= 1) return; // Keep at least one layer
    onLayersChange(layers.filter((_, i) => i !== index));
  }, [layers, onLayersChange]);

  // Move layer up/down
  const moveLayer = useCallback((index: number, direction: 'up' | 'down') => {
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= layers.length) return;

    const newLayers = [...layers];
    [newLayers[index], newLayers[newIndex]] = [newLayers[newIndex], newLayers[index]];
    onLayersChange(newLayers);
  }, [layers, onLayersChange]);

  // Clone a layer (insert copy below)
  const cloneLayer = useCallback((index: number) => {
    const layerToClone = layers[index];
    const clonedLayer: Layer = {
      depth: layerToClone.depth,
      ...(layerToClone.shape && { shape: layerToClone.shape }),
      ...(layerToClone.attach_next_at !== undefined && { attach_next_at: layerToClone.attach_next_at }),
      ...(layerToClone.branch_directions && { branch_directions: [...layerToClone.branch_directions] }),
      ...(layerToClone.branch_style && { branch_style: layerToClone.branch_style }),
    };
    const newLayers = [...layers];
    newLayers.splice(index + 1, 0, clonedLayer);
    onLayersChange(newLayers);
  }, [layers, onLayersChange]);

  // Generate attach point options for a layer (1 to depth)
  const getAttachOptions = (layerDepth: number) =>
    Array.from({ length: layerDepth }, (_, i) => i + 1);

  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Label className="text-base">Layers</Label>
        </div>
        <Button onClick={addLayer} size="sm" variant="secondary">
          <Plus className="h-3 w-3 mr-1" />
          Add
        </Button>
      </div>

      {/* Layers */}
      <div className="space-y-3">
        {layers.map((layer, index) => {
          const attachOptions = getAttachOptions(layer.depth);
          const currentAttach = layer.attach_next_at ?? layer.depth; // Default to top

          return (
            <div key={index} className="bg-muted/50 p-3 rounded-lg border border-border/50 space-y-3">
              {/* Layer header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-primary">Layer {index + 1}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Button
                    variant="ghost"
                    size="icon-sm"
                    onClick={() => cloneLayer(index)}
                    className="text-muted-foreground hover:text-foreground h-6 w-6"
                    title="Clone layer"
                  >
                    <Copy className="h-3 w-3" />
                  </Button>
                  {layers.length > 1 && (
                    <>
                      <Button
                        variant="ghost"
                        size="icon-sm"
                        onClick={() => moveLayer(index, 'up')}
                        disabled={index === 0}
                        className="text-muted-foreground hover:text-foreground h-6 w-6"
                      >
                        <ChevronUp className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon-sm"
                        onClick={() => moveLayer(index, 'down')}
                        disabled={index === layers.length - 1}
                        className="text-muted-foreground hover:text-foreground h-6 w-6"
                      >
                        <ChevronDown className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon-sm"
                        onClick={() => removeLayer(index)}
                        className="text-muted-foreground hover:text-destructive h-6 w-6"
                      >
                        <X className="h-3 w-3" />
                      </Button>
                    </>
                  )}
                </div>
              </div>

              {/* Depth selector */}
              <div className="flex items-center gap-2">
                <Label className="text-xs w-12">Depth</Label>
                <div className="flex gap-1">
                  {[1, 2, 3, 4, 5].map((d) => (
                    <Button
                      key={d}
                      variant={layer.depth === d ? "default" : "outline"}
                      size="sm"
                      className="h-6 w-6 p-0 text-xs"
                      onClick={() => updateLayer(index, { depth: d })}
                    >
                      {d}
                    </Button>
                  ))}
                </div>
              </div>

              {/* Shape selector */}
              <div className="flex items-center gap-2">
                <Label className="text-xs w-12">Shape</Label>
                <ToggleGroup
                  type="single"
                  value={layer.shape || 'fractal'}
                  onValueChange={(value) => {
                    if (value) {
                      updateLayer(index, { shape: value as LayerShape });
                    }
                  }}
                  variant="outline"
                  className="justify-start"
                >
                  {LAYER_SHAPE_OPTIONS.map((opt) => (
                    <ToggleGroupItem
                      key={opt.value}
                      value={opt.value}
                      size="sm"
                      className="text-xs px-2 h-6 data-[state=on]:bg-primary data-[state=on]:text-primary-foreground"
                      title={opt.description}
                    >
                      {opt.label}
                    </ToggleGroupItem>
                  ))}
                </ToggleGroup>
              </div>

              {/* Attach point selector (only show if not the last layer) */}
              {index < layers.length - 1 && (
                <div className="flex items-center gap-2">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Label className="text-xs w-12 cursor-help">Attach</Label>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Next layer attaches at this depth level</p>
                    </TooltipContent>
                  </Tooltip>
                  <div className="flex gap-1">
                    {attachOptions.map((d) => (
                      <Button
                        key={d}
                        variant={currentAttach === d ? "default" : "outline"}
                        size="sm"
                        className="h-6 w-6 p-0 text-xs"
                        onClick={() => updateLayer(index, { attach_next_at: d })}
                      >
                        {d}
                      </Button>
                    ))}
                  </div>
                </div>
              )}

              {/* Branch directions */}
              <div className="flex items-center gap-2">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Label className="text-xs w-12 cursor-help">Branch</Label>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Spawn sub-structures in these directions</p>
                  </TooltipContent>
                </Tooltip>
                <ToggleGroup
                  type="multiple"
                  value={layer.branch_directions || ['upwards']}
                  onValueChange={(value) => {
                    // Require at least one selection - if empty, keep current value
                    if (value.length === 0) return;
                    updateLayer(index, { branch_directions: value as BranchDirection[] });
                  }}
                  variant="outline"
                  className="justify-start"
                >
                  {BRANCH_DIRECTION_OPTIONS.map((opt) => (
                    <ToggleGroupItem
                      key={opt.value}
                      value={opt.value}
                      size="sm"
                      className="text-xs px-2 h-6 data-[state=on]:bg-primary data-[state=on]:text-primary-foreground"
                      title={opt.description}
                    >
                      {opt.label}
                    </ToggleGroupItem>
                  ))}
                </ToggleGroup>
              </div>

              {/* Branch style - only show when there are horizontal branches */}
              {layer.branch_directions && layer.branch_directions.some(d => d !== 'upwards') && (
                <div className="flex items-center gap-2">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Label className="text-xs w-12 cursor-help">Style</Label>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>How sub-structures are built</p>
                    </TooltipContent>
                  </Tooltip>
                  <ToggleGroup
                    type="single"
                    value={layer.branch_style || 'evil'}
                    onValueChange={(value) => {
                      if (value) {
                        updateLayer(index, { branch_style: value as BranchStyle });
                      }
                    }}
                    variant="outline"
                    className="justify-start"
                  >
                    {BRANCH_STYLE_OPTIONS.map((opt) => (
                      <ToggleGroupItem
                        key={opt.value}
                        value={opt.value}
                        size="sm"
                        className="text-xs px-2 h-6 data-[state=on]:bg-primary data-[state=on]:text-primary-foreground"
                        title={opt.description}
                      >
                        {opt.label}
                      </ToggleGroupItem>
                    ))}
                  </ToggleGroup>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
