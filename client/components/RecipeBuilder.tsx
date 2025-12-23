'use client';

import { useCallback } from 'react';
import { Layer, DepthRule, NodeType, NODE_TYPES, BranchDirection, ALL_BRANCH_DIRECTIONS } from '@/lib/api';

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
  // Calculate max depth from layers
  const maxDepth = Math.max(...layers.map(l => l.depth), 1);

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

  // Generate depth levels from maxDepth down to 1
  const depthLevels = Array.from({ length: maxDepth }, (_, i) => maxDepth - i);

  return (
    <div className="space-y-4">
      {/* Layers section */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="text-sm font-medium">Layers</label>
          <button
            onClick={addLayer}
            className="text-xs px-2 py-1 bg-purple-600 hover:bg-purple-700 rounded transition-colors"
          >
            + Add Layer
          </button>
        </div>
        <p className="text-xs text-gray-400 mb-2">
          Stack flakes vertically (like Tower/Star)
        </p>

        <div className="space-y-2">
          {layers.map((layer, index) => (
            <div key={index} className="bg-gray-800/50 p-2 rounded">
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500 w-4">{index + 1}</span>

                <div className="flex-1 space-y-1">
                  <div className="flex items-center gap-2">
                    <label className="text-xs text-gray-400 w-12">Depth:</label>
                    <input
                      type="range"
                      min={1}
                      max={5}
                      value={layer.depth}
                      onChange={(e) => updateLayer(index, { depth: Number(e.target.value) })}
                      className="flex-1"
                    />
                    <span className="text-xs w-4">{layer.depth}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <label className="text-xs text-gray-400 w-12">Fill:</label>
                    <input
                      type="range"
                      min={0}
                      max={layer.depth}
                      value={layer.fill_depth}
                      onChange={(e) => updateLayer(index, { fill_depth: Number(e.target.value) })}
                      className="flex-1"
                    />
                    <span className="text-xs w-4">{layer.fill_depth}</span>
                  </div>

                  {/* Branches toggle - only show if there are more layers below */}
                  {index < layers.length - 1 && (
                    <>
                      <div className="flex items-center gap-2">
                        <label className="text-xs text-gray-400 w-12">Branch:</label>
                        <button
                          onClick={() => updateLayer(index, { branches: !layer.branches })}
                          className={`px-2 py-0.5 text-xs rounded transition-colors ${
                            layer.branches
                              ? 'bg-purple-600 text-white'
                              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                          }`}
                          title="Spawn sub-structures in horizontal directions"
                        >
                          {layer.branches ? 'On' : 'Off'}
                        </button>
                        <span className="text-xs text-gray-500">Spawn horizontal sub-towers</span>
                      </div>

                      {/* Branch options - only show when branches enabled */}
                      {layer.branches && (
                        <>
                          {/* Direction toggles */}
                          <div className="flex items-center gap-2 ml-4">
                            <label className="text-xs text-gray-400 w-8">Dirs:</label>
                            <div className="flex gap-1">
                              {ALL_BRANCH_DIRECTIONS.map((dir) => {
                                const currentDirs = layer.branch_directions || ALL_BRANCH_DIRECTIONS;
                                const isActive = currentDirs.includes(dir);
                                return (
                                  <button
                                    key={dir}
                                    onClick={() => {
                                      let newDirs: BranchDirection[];
                                      if (isActive) {
                                        // Remove direction (but keep at least one)
                                        newDirs = currentDirs.filter(d => d !== dir);
                                        if (newDirs.length === 0) newDirs = [dir];
                                      } else {
                                        // Add direction
                                        newDirs = [...currentDirs, dir];
                                      }
                                      updateLayer(index, { branch_directions: newDirs });
                                    }}
                                    className={`px-1.5 py-0.5 text-xs rounded font-mono transition-colors ${
                                      isActive
                                        ? 'bg-green-600 text-white'
                                        : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                                    }`}
                                    title={`Branch in ${dir} direction`}
                                  >
                                    {dir}
                                  </button>
                                );
                              })}
                            </div>
                          </div>

                          {/* Exclude origin toggle */}
                          <div className="flex items-center gap-2 ml-4">
                            <label className="text-xs text-gray-400 w-8">Orbit:</label>
                            <button
                              onClick={() => updateLayer(index, {
                                branch_exclude_origin: layer.branch_exclude_origin === false
                              })}
                              className={`px-2 py-0.5 text-xs rounded transition-colors ${
                                layer.branch_exclude_origin !== false
                                  ? 'bg-green-600 text-white'
                                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                              }`}
                              title="Symmetric orbiting: each sub-branch can't branch back toward its parent"
                            >
                              {layer.branch_exclude_origin !== false ? 'On' : 'Off'}
                            </button>
                            <span className="text-xs text-gray-500">
                              {layer.branch_exclude_origin !== false
                                ? 'Symmetric (no back-branching)'
                                : 'Asymmetric (can overlap)'}
                            </span>
                          </div>
                        </>
                      )}
                    </>
                  )}
                </div>

                {layers.length > 1 && (
                  <button
                    onClick={() => removeLayer(index)}
                    className="text-gray-500 hover:text-red-400 transition-colors self-start mt-1"
                    title="Remove layer"
                  >
                    ×
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Depth rules section */}
      <div>
        <label className="block text-sm font-medium mb-2">Depth Rules</label>
        <p className="text-xs text-gray-400 mb-3">
          Modify branching behavior at each depth level
        </p>

        <div className="space-y-2">
          {depthLevels.map((depth) => {
            const currentType = getRuleForDepth(depth);
            const isDefault = currentType === 'flake';

            return (
              <div key={depth} className="flex items-center gap-2">
                <span className={`w-6 text-center text-sm font-mono ${
                  isDefault ? 'text-gray-500' : 'text-purple-400'
                }`}>
                  {depth}
                </span>
                <div className="flex-1 flex gap-1 flex-wrap">
                  {NODE_TYPES.map((nodeType) => (
                    <button
                      key={nodeType.value}
                      onClick={() => setRuleForDepth(depth, nodeType.value)}
                      className={`px-2 py-1 text-xs rounded transition-colors ${
                        currentType === nodeType.value
                          ? nodeType.value === 'flake'
                            ? 'bg-gray-600 text-white'
                            : 'bg-purple-600 text-white'
                          : 'bg-gray-800 hover:bg-gray-700 text-gray-300'
                      }`}
                      title={nodeType.description}
                    >
                      {nodeType.label}
                    </button>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Summary */}
      {(layers.length > 1 || depthRules.length > 0 || layers.some(l => l.branches)) && (
        <div className="text-xs text-gray-400 bg-gray-800/50 p-2 rounded space-y-1">
          {layers.length > 1 && (
            <div>
              <span className="font-medium text-gray-300">Layers:</span>{' '}
              {layers.map((l, i) => (
                <span key={i}>
                  {i > 0 && ' → '}
                  <span className="text-purple-400">D{l.depth}</span>
                  {l.fill_depth > 0 && <span className="text-gray-500">(fill:{l.fill_depth})</span>}
                  {l.branches && <span className="text-green-400">*</span>}
                </span>
              ))}
              {layers.some(l => l.branches) && (
                <span className="text-gray-500 ml-1">(*=branches)</span>
              )}
            </div>
          )}
          {depthRules.length > 0 && (
            <div>
              <span className="font-medium text-gray-300">Rules:</span>{' '}
              {depthRules.map((rule, i) => (
                <span key={rule.depth}>
                  {i > 0 && ', '}
                  <span className="text-purple-400">D{rule.depth}</span>→{rule.type}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Help text */}
      <div className="text-xs text-gray-500 space-y-1">
        <p><strong>Fractal:</strong> Standard 6-way branching</p>
        <p><strong>Solid:</strong> Fill solid, stop recursion</p>
        <p><strong>Flat:</strong> Horizontal only (disc layers)</p>
        <p><strong>Spire:</strong> Vertical only (columns)</p>
        <p><strong>Skip:</strong> Skip this level, continue deeper</p>
      </div>
    </div>
  );
}
