'use client';

import { useCallback } from 'react';
import { Plus, X, ChevronDown, ChevronUp, Copy } from 'lucide-react';
import { Layer, LayerShape, SpawnDirection, LAYER_SHAPE_OPTIONS, SPAWN_DIRECTION_OPTIONS } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Toggle } from '@/components/ui/toggle';
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
      ...(layerToClone.spawn && { spawn: [...layerToClone.spawn] }),
      ...(layerToClone.bloom && { bloom: layerToClone.bloom }),
      ...(layerToClone.echo && { echo: layerToClone.echo }),
    };
    const newLayers = [...layers];
    newLayers.splice(index + 1, 0, clonedLayer);
    onLayersChange(newLayers);
  }, [layers, onLayersChange]);

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
        {layers.map((layer, index) => (
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

              {/* Size selector */}
              <div className="flex items-center gap-2">
                <Label className="text-xs w-12">Size</Label>
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
                  value={[layer.shape || 'fractal']}
                  onValueChange={(value) => {
                    if (value.length > 0) {
                      updateLayer(index, { shape: value[0] as LayerShape });
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
                      className="text-xs px-2 h-6 data-[pressed]:bg-primary data-[pressed]:text-primary-foreground"
                      title={opt.description}
                    >
                      {opt.label}
                    </ToggleGroupItem>
                  ))}
                </ToggleGroup>
              </div>

              {/* Spawn directions */}
              <div className="flex items-center gap-2">
                <Tooltip>
                  <TooltipTrigger render={<Label className="text-xs w-12 cursor-help" />}>
                    Spawn
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Where to create sub-structures horizontally</p>
                  </TooltipContent>
                </Tooltip>
                <ToggleGroup
                  multiple
                  value={layer.spawn || []}
                  onValueChange={(value) => {
                    updateLayer(index, { spawn: value.length > 0 ? value as SpawnDirection[] : undefined });
                  }}
                  variant="outline"
                  className="justify-start"
                >
                  {SPAWN_DIRECTION_OPTIONS.map((opt) => (
                    <ToggleGroupItem
                      key={opt.value}
                      value={opt.value}
                      size="sm"
                      className="text-xs px-2 h-6 data-[pressed]:bg-primary data-[pressed]:text-primary-foreground"
                      title={opt.description}
                    >
                      {opt.label}
                    </ToggleGroupItem>
                  ))}
                </ToggleGroup>
              </div>

              {/* Bloom and Echo - only show when spawns are enabled */}
              {layer.spawn && layer.spawn.length > 0 && (
                <div className="flex items-center gap-4">
                  <Tooltip>
                    <TooltipTrigger render={<div className="flex items-center gap-2" />}>
                      <Label className="text-xs cursor-help">Bloom</Label>
                      <Toggle
                        pressed={layer.bloom || false}
                        onPressedChange={(pressed) => {
                          updateLayer(index, { bloom: pressed, echo: pressed ? false : layer.echo });
                        }}
                        size="sm"
                        className="h-6 text-xs data-[pressed]:bg-primary data-[pressed]:text-primary-foreground"
                      >
                        {layer.bloom ? 'On' : 'Off'}
                      </Toggle>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Spawns continue branching recursively (like Flower)</p>
                    </TooltipContent>
                  </Tooltip>

                  <Tooltip>
                    <TooltipTrigger render={<div className="flex items-center gap-2" />}>
                      <Label className="text-xs cursor-help">Echo</Label>
                      <Toggle
                        pressed={layer.echo || false}
                        onPressedChange={(pressed) => {
                          updateLayer(index, { echo: pressed, bloom: pressed ? false : layer.bloom });
                        }}
                        size="sm"
                        className="h-6 text-xs data-[pressed]:bg-primary data-[pressed]:text-primary-foreground"
                      >
                        {layer.echo ? 'On' : 'Off'}
                      </Toggle>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Spawns contain full recipe at smaller scale (like Temple Complex)</p>
                    </TooltipContent>
                  </Tooltip>
                </div>
              )}
            </div>
        ))}
      </div>
    </div>
  );
}
