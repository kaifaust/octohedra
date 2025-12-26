'use client';

import { useState, useEffect } from 'react';
import { ChevronRight, ChevronLeft, Loader2 } from 'lucide-react';
import { StoredShape, listRecentShapes, Layer } from '@/lib/api';
import { Button } from '@/components/ui/button';

interface RecentShapesPanelProps {
  onSelectShape: (layers: Layer[], sixWay: boolean) => void;
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
}

export function RecentShapesPanel({ onSelectShape, isOpen, onOpenChange }: RecentShapesPanelProps) {
  const [shapes, setShapes] = useState<StoredShape[]>([]);
  const [isLoading, setIsLoading] = useState(true);
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

  // Layout approach:
  // - Use a flex column container anchored to the right edge
  // - Desktop: top-4, with bottom padding for fileInfoBar (bottom-4 + bar height ~2rem = 6rem total)
  // - Mobile: below fileInfoBar (top-14), with bottom padding for MobileBottomSheet header (~4rem)
  // - z-50 to stay above MobileBottomSheet (z-40)

  return (
    <div className="absolute top-14 md:top-4 right-4 bottom-20 md:bottom-12 z-50 flex flex-col items-end gap-2 pointer-events-none">
      {/* Toggle button */}
      <Button
        variant="secondary"
        size="icon"
        className="bg-card/80 backdrop-blur-sm border-border/50 pointer-events-auto shrink-0"
        onClick={() => onOpenChange(!isOpen)}
        aria-label={isOpen ? 'Close recent shapes' : 'Show recent shapes'}
      >
        {isOpen ? (
          <ChevronRight className="h-4 w-4" />
        ) : (
          <ChevronLeft className="h-4 w-4" />
        )}
      </Button>

      {/* Panel - uses remaining space in the flex container */}
      <div
        className={`w-24 min-h-0 flex-1 transition-all duration-200 ease-in-out pointer-events-auto ${
          isOpen ? 'opacity-100' : 'translate-x-full opacity-0 pointer-events-none'
        }`}
      >
        <div className="bg-card/80 backdrop-blur-sm border border-border/50 rounded-lg p-2 max-h-full overflow-y-auto">
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
    </div>
  );
}
