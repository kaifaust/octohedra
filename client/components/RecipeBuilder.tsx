'use client';

import { useCallback } from 'react';
import { Plus, X, ChevronDown, ChevronUp } from 'lucide-react';
import { Layer, DepthRule, NodeType, NODE_TYPES, BranchDirection, ALL_BRANCH_DIRECTIONS } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

interface RecipeBuilderProps {
  layers: Layer[];
  depthRules: DepthRule[];
  onLayersChange: (layers: Layer[]) => void;
  onDepthRulesChange: (rules: DepthRule[]) => void;
}

export function RecipeBuilder({
  layers,
  depthRules,
  onLayersChange,
  onDepthRulesChange,
}: RecipeBuilderProps) {
  // Get the depth rule for a specific depth
  const getRuleForDepth = useCallback((depth: number): NodeType => {
    const rule = depthRules.find(r => r.depth === depth);
    return rule?.type || 'flake';
  }, [depthRules]);

  // Update or add a depth rule
  const setRuleForDepth = useCallback((depth: number, type: NodeType) => {
    let newRules: DepthRule[];

    if (type === 'flake') {
      // Remove the rule if setting back to default
      newRules = depthRules.filter(r => r.depth !== depth);
    } else {
      const existing = depthRules.find(r => r.depth === depth);
      if (existing) {
        newRules = depthRules.map(r =>
          r.depth === depth ? { depth, type } : r
        );
      } else {
        newRules = [...depthRules, { depth, type }];
      }
    }

    onDepthRulesChange(newRules);
  }, [depthRules, onDepthRulesChange]);

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
    onLayersChange([...layers, { depth: newDepth, fill_depth: 0 }]);
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

  // Generate depth levels for a layer (from layer.depth down to 1)
  const getDepthLevels = (layerDepth: number) =>
    Array.from({ length: layerDepth }, (_, i) => layerDepth - i);

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
                  <span className="text-xs text-muted-foreground">
                    Depth {layer.depth}{layer.fill_depth > 0 ? `, Fill ${layer.fill_depth}` : ''}
                  </span>
                </div>
                <div className="flex items-center gap-1">
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

              {/* Depth & Fill sliders side by side */}
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1">
                  <div className="flex items-center justify-between">
                    <Label className="text-xs">Depth</Label>
                    <span className="text-xs font-mono text-muted-foreground">{layer.depth}</span>
                  </div>
                  <Slider
                    min={1}
                    max={5}
                    step={1}
                    value={[layer.depth]}
                    onValueChange={([value]) => updateLayer(index, { depth: value })}
                  />
                </div>
                <div className="space-y-1">
                  <div className="flex items-center justify-between">
                    <Label className="text-xs">Fill</Label>
                    <span className="text-xs font-mono text-muted-foreground">{layer.fill_depth}</span>
                  </div>
                  <Slider
                    min={0}
                    max={layer.depth}
                    step={1}
                    value={[layer.fill_depth]}
                    onValueChange={([value]) => updateLayer(index, { fill_depth: value })}
                  />
                </div>
              </div>

              {/* Depth rules for this layer */}
              <div className="space-y-2">
                <Label className="text-xs text-muted-foreground">Node Types by Depth</Label>
                <div className="space-y-1.5">
                  {depthLevels.map((depth) => {
                    const currentType = getRuleForDepth(depth);
                    const isDefault = currentType === 'flake';

                    return (
                      <div key={depth} className="flex items-center gap-2">
                        <span className={`w-5 text-center text-xs font-mono ${
                          isDefault ? 'text-muted-foreground' : 'text-primary'
                        }`}>
                          {depth}
                        </span>
                        <ToggleGroup
                          type="single"
                          value={currentType}
                          onValueChange={(value) => {
                            if (value) setRuleForDepth(depth, value as NodeType);
                          }}
                          variant="outline"
                          className="flex-1 justify-start gap-1"
                        >
                          {NODE_TYPES.map((nodeType) => (
                            <Tooltip key={nodeType.value}>
                              <TooltipTrigger asChild>
                                <ToggleGroupItem
                                  value={nodeType.value}
                                  size="sm"
                                  className={`text-xs h-6 px-2 ${
                                    currentType === nodeType.value
                                      ? 'bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground'
                                      : ''
                                  }`}
                                >
                                  {nodeType.label}
                                </ToggleGroupItem>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>{nodeType.description}</p>
                              </TooltipContent>
                            </Tooltip>
                          ))}
                        </ToggleGroup>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Branches toggle - only show if there are more layers below */}
              {index < layers.length - 1 && (
                <div className="space-y-2 pt-1 border-t border-border/30">
                  <div className="flex items-center gap-2 pt-2">
                    <Switch
                      checked={layer.branches ?? false}
                      onCheckedChange={(checked) => updateLayer(index, { branches: checked })}
                    />
                    <Label className="text-xs">Branch to sub-layers</Label>
                  </div>

                  {/* Branch options - only show when branches enabled */}
                  {layer.branches && (
                    <div className="ml-6 space-y-2">
                      {/* Direction toggles */}
                      <div className="space-y-1">
                        <Label className="text-xs text-muted-foreground">Directions</Label>
                        <ToggleGroup
                          type="multiple"
                          value={layer.branch_directions || ALL_BRANCH_DIRECTIONS}
                          onValueChange={(value) => {
                            if (value.length > 0) {
                              updateLayer(index, { branch_directions: value as BranchDirection[] });
                            }
                          }}
                          variant="outline"
                          className="justify-start gap-1"
                        >
                          {ALL_BRANCH_DIRECTIONS.map((dir) => {
                            const isSelected = (layer.branch_directions || ALL_BRANCH_DIRECTIONS).includes(dir);
                            return (
                              <ToggleGroupItem
                                key={dir}
                                value={dir}
                                size="sm"
                                className={`font-mono text-xs px-2 h-6 ${
                                  isSelected
                                    ? 'bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground'
                                    : ''
                                }`}
                              >
                                {dir}
                              </ToggleGroupItem>
                            );
                          })}
                        </ToggleGroup>
                      </div>

                      {/* Orbit toggle */}
                      <div className="flex items-center gap-2">
                        <Switch
                          checked={layer.branch_exclude_origin !== false}
                          onCheckedChange={(checked) => updateLayer(index, { branch_exclude_origin: checked })}
                        />
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Label className="text-xs cursor-help">
                              Orbit mode
                            </Label>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Sub-branches can&apos;t branch back toward parent</p>
                          </TooltipContent>
                        </Tooltip>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
