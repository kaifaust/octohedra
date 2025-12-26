'use client';

import { useState, useEffect } from 'react';
import { ChevronRight, ChevronLeft, Loader2 } from 'lucide-react';
import { StoredShape, listRecentShapes, Layer } from '@/lib/api';
import { Button } from '@/components/ui/button';

interface RecentShapesPanelProps {
  onSelectShape: (layers: Layer[], sixWay: boolean) => void;
}

export function RecentShapesPanel({ onSelectShape }: RecentShapesPanelProps) {
  const [shapes, setShapes] = useState<StoredShape[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchShapes() {
      try {
        setIsLoading(true);
        const recentShapes = await listRecentShapes(10);
        setShapes(recentShapes);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch recent shapes:', err);
        setError('Failed to load');
      } finally {
        setIsLoading(false);
      }
    }

    fetchShapes();
  }, []);

  // Don't render panel if there's an error or no shapes
  if (error || (!isLoading && shapes.length === 0)) {
    return null;
  }

  return (
    <>
      {/* Toggle button - positioned to avoid conflicts with file info bar */}
      {/* Mobile: below file info (top-14), Desktop: bottom-right above file info bar */}
      <Button
        variant="secondary"
        size="icon"
        className="absolute top-14 right-4 md:top-4 bg-card/80 backdrop-blur-sm border-border/50 z-10"
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close recent shapes' : 'Show recent shapes'}
      >
        {isOpen ? (
          <ChevronRight className="h-4 w-4" />
        ) : (
          <ChevronLeft className="h-4 w-4" />
        )}
      </Button>

      {/* Panel */}
      <div
        className={`absolute top-24 md:top-14 right-4 w-24 transition-transform duration-200 ease-in-out ${
          isOpen ? 'translate-x-0' : 'translate-x-full opacity-0 pointer-events-none'
        }`}
      >
        <div className="bg-card/80 backdrop-blur-sm border border-border/50 rounded-lg p-2 max-h-[calc(100dvh-8rem)] md:max-h-[calc(100dvh-5rem)] overflow-y-auto">
          <h3 className="text-xs font-medium text-muted-foreground mb-2 px-1">Recent</h3>

          {isLoading ? (
            <div className="flex items-center justify-center py-4">
              <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
            </div>
          ) : (
            <div className="space-y-2">
              {shapes.map((shape) => (
                <button
                  key={shape.id}
                  onClick={() => onSelectShape(shape.layers, shape.sixWay)}
                  className="w-full aspect-square rounded-md overflow-hidden border border-border/50 hover:border-primary/50 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50"
                >
                  <img
                    src={shape.screenshotUrl}
                    alt="Shape preview"
                    className="w-full h-full object-cover"
                    loading="lazy"
                  />
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
