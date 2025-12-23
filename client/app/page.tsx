'use client';

import { useState, useEffect } from 'react';
import { FractalViewer } from '@/components/FractalViewer';
import { useFractalGeneration } from '@/hooks/useFractalGeneration';

export default function Home() {
  const [iteration, setIteration] = useState(2);
  const [scale, setScale] = useState(0);

  const { objData, isLoading, error, generate } = useFractalGeneration();

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
    generate({ iteration: 2, scale: 0 });
  }, [generate]);

  const handleGenerate = () => {
    generate({ iteration, scale });
  };

  return (
    <main className="relative w-full h-dvh overflow-hidden">
      {/* Full-screen 3D Viewer */}
      <FractalViewer objData={objData} />

      {/* Overlay Controls */}
      <div className="absolute top-4 left-4 w-64 p-4 bg-gray-900/80 backdrop-blur-sm rounded-lg text-white space-y-4">
        <h1 className="text-xl font-bold">Octoflake</h1>

        <div>
          <label className="block text-sm font-medium mb-1">
            Iteration: {iteration}
          </label>
          <input
            type="range"
            min={1}
            max={5}
            value={iteration}
            onChange={(e) => setIteration(Number(e.target.value))}
            className="w-full"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Scale: {scale}
          </label>
          <input
            type="range"
            min={0}
            max={3}
            value={scale}
            onChange={(e) => setScale(Number(e.target.value))}
            className="w-full"
          />
        </div>

        <button
          onClick={handleGenerate}
          disabled={isLoading}
          className="w-full py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded font-semibold transition-colors"
        >
          {isLoading ? 'Generating...' : 'Generate'}
        </button>

        {error && (
          <p className="text-red-400 text-xs bg-red-900/30 p-2 rounded">
            {error.message}
          </p>
        )}

        {objData && (
          <p className="text-green-400 text-xs">
            {Math.round(objData.length / 1024)}KB loaded
          </p>
        )}
      </div>
    </main>
  );
}
