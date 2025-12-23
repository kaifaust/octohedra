'use client';

import { useCallback } from 'react';
import { Plus, X, ChevronDown, ChevronUp, Copy } from 'lucide-react';
import { Layer, DepthRule, NodeType, BranchDirection, BRANCH_DIRECTION_OPTIONS, nodeTypeToBranching, branchingToNodeType } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
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
  // Get the depth rule for a specific layer and depth
  const getRuleForDepth = useCallback((layerIndex: number, depth: number): NodeType => {
    const layerRules = layers[layerIndex]?.depth_rules || [];
    const rule = layerRules.find(r => r.depth === depth);
    return rule?.type || 'flake';
  }, [layers]);

  // Update or add a depth rule for a specific layer
  const setRuleForDepth = useCallback((layerIndex: number, depth: number, type: NodeType) => {
    const layer = layers[layerIndex];
    const currentRules = layer.depth_rules || [];
    let newRules: DepthRule[];

    if (type === 'flake') {
      // Remove the rule if setting back to default
      newRules = currentRules.filter(r => r.depth !== depth);
    } else {
      const existing = currentRules.find(r => r.depth === depth);
      if (existing) {
        newRules = currentRules.map(r =>
          r.depth === depth ? { depth, type } : r
        );
      } else {
        newRules = [...currentRules, { depth, type }];
      }
    }

    // Update the layer with the new rules
    const newLayers = layers.map((l, i) =>
      i === layerIndex ? { ...l, depth_rules: newRules.length > 0 ? newRules : undefined } : l
    );
    onLayersChange(newLayers);
  }, [layers, onLayersChange]);

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
    // Deep clone to avoid shared references
    const clonedLayer: Layer = {
      depth: layerToClone.depth,
      ...(layerToClone.attach_next_at !== undefined && { attach_next_at: layerToClone.attach_next_at }),
      ...(layerToClone.branch_directions && { branch_directions: [...layerToClone.branch_directions] }),
      ...(layerToClone.depth_rules && { depth_rules: layerToClone.depth_rules.map(r => ({ ...r })) }),
    };
    const newLayers = [...layers];
    newLayers.splice(index + 1, 0, clonedLayer);
    onLayersChange(newLayers);
  }, [layers, onLayersChange]);

  // Generate depth levels for a layer (from 1 up to layer.depth)
  const getDepthLevels = (layerDepth: number) =>
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
          const depthLevels = getDepthLevels(layer.depth);

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
                <Label className="text-xs">Depth</Label>
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

              {/* Depth rules for this layer - octahedron branching per depth */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label className="text-xs text-muted-foreground">Octahedra at each depth</Label>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Label className="text-xs text-muted-foreground cursor-help">Attach</Label>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Next layer attaches at checked depth</p>
                    </TooltipContent>
                  </Tooltip>
                </div>
                <div className="space-y-1.5">
                  {depthLevels.map((depth) => {
                    const currentType = getRuleForDepth(index, depth);
                    const { horizontal, vertical, fill } = nodeTypeToBranching(currentType);
                    // Default attach point is the top (layer.depth) when attach_next_at is undefined
                    const isAttachPoint = layer.attach_next_at === depth ||
                      (layer.attach_next_at === undefined && depth === layer.depth);

                    const updateBranching = (h: boolean, v: boolean, f: boolean) => {
                      const newType = branchingToNodeType(h, v, f);
                      setRuleForDepth(index, depth, newType);
                    };

                    return (
                      <div key={depth} className="flex items-center gap-3">
                        <span className="w-4 text-center text-xs font-mono text-muted-foreground">
                          {depth}
                        </span>
                        <div className="flex items-center gap-3 flex-1">
                          <label className="flex items-center gap-1.5 cursor-pointer">
                            <Checkbox
                              checked={horizontal && !fill}
                              onCheckedChange={(checked) => {
                                // Clicking H turns off fill
                                updateBranching(!!checked, vertical, false);
                              }}
                            />
                            <span className="text-xs">H</span>
                          </label>
                          <label className="flex items-center gap-1.5 cursor-pointer">
                            <Checkbox
                              checked={vertical && !fill}
                              onCheckedChange={(checked) => {
                                // Clicking V turns off fill
                                updateBranching(horizontal, !!checked, false);
                              }}
                            />
                            <span className="text-xs">V</span>
                          </label>
                          <label className="flex items-center gap-1.5 cursor-pointer">
                            <Checkbox
                              checked={fill}
                              onCheckedChange={(checked) => {
                                if (checked) {
                                  // Enable fill (turns off H and V)
                                  updateBranching(false, false, true);
                                } else {
                                  // Disable fill - restore to default (both H and V)
                                  updateBranching(true, true, false);
                                }
                              }}
                            />
                            <span className="text-xs text-muted-foreground">Fill</span>
                          </label>
                        </div>
                        <Checkbox
                          checked={isAttachPoint}
                          onCheckedChange={(checked) => {
                            updateLayer(index, {
                              attach_next_at: checked ? depth : undefined
                            });
                          }}
                        />
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Branch directions */}
              <div className="space-y-2 pt-1 border-t border-border/30">
                <div className="pt-2">
                  <Label className="text-xs text-muted-foreground">Branch to sub-layers</Label>
                </div>
                <ToggleGroup
                  type="multiple"
                  value={layer.branch_directions || []}
                  onValueChange={(value) => {
                    updateLayer(index, { branch_directions: value.length > 0 ? value as BranchDirection[] : undefined });
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
            </div>
          );
        })}
      </div>
    </div>
  );
}
