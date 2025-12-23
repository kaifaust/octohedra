'use client';

import { useState } from 'react';
import { FractalViewer } from '@/components/FractalViewer';
import { useFractalGeneration } from '@/hooks/useFractalGeneration';

export default function Home() {
  const [iteration, setIteration] = useState(2);
  const [scale, setScale] = useState(0);

  const { objData, isLoading, error, generate } = useFractalGeneration();

  const handleGenerate = () => {
    generate({ iteration, scale });
  };

  return (
    <main className="min-h-screen p-8 bg-gray-950 text-white">
      <h1 className="text-4xl font-bold mb-8">Octoflake Viewer</h1>

      <div className="flex gap-8">
        {/* Control Panel */}
        <div className="w-64 space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">
              Iteration (1-5)
            </label>
            <input
              type="range"
              min={1}
              max={5}
              value={iteration}
              onChange={(e) => setIteration(Number(e.target.value))}
              className="w-full"
            />
            <span className="text-lg font-mono">{iteration}</span>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Scale (0-3)
            </label>
            <input
              type="range"
              min={0}
              max={3}
              value={scale}
              onChange={(e) => setScale(Number(e.target.value))}
              className="w-full"
            />
            <span className="text-lg font-mono">{scale}</span>
          </div>

          <button
            onClick={handleGenerate}
            disabled={isLoading}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded font-semibold transition-colors"
          >
            {isLoading ? 'Generating...' : 'Generate Fractal'}
          </button>

          {error && (
            <p className="text-red-400 text-sm bg-red-900/20 p-2 rounded">
              {error.message}
            </p>
          )}

          {objData && (
            <p className="text-green-400 text-sm">
              Model loaded ({Math.round(objData.length / 1024)}KB)
            </p>
          )}
        </div>

        {/* 3D Viewer */}
        <div className="flex-1">
          <FractalViewer objData={objData} />
        </div>
      </div>
    </main>
  );
}
