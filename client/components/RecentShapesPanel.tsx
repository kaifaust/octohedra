'use client';

import { useState, useEffect, useCallback, useImperativeHandle, forwardRef } from 'react';
import { ChevronRight, ChevronLeft, Loader2 } from 'lucide-react';
import { StoredShape, listRecentShapes, Layer } from '@/lib/api';
import { Button } from '@/components/ui/button';

interface RecentShapesPanelProps {
  onSelectShape: (layers: Layer[], sixWay: boolean) => void;
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
}

export interface RecentShapesPanelHandle {
  refresh: () => Promise<void>;
}

// Module-level state to dedupe fetches across mounts
const fetchState = {
  promise: null as Promise<StoredShape[]> | null,
  data: null as StoredShape[] | null,
};

export const RecentShapesPanel = forwardRef<RecentShapesPanelHandle, RecentShapesPanelProps>(
  function RecentShapesPanel({ onSelectShape, isOpen, onOpenChange }, ref) {
  // Initialize from cached data if available
  const [shapes, setShapes] = useState<StoredShape[]>(() => fetchState.data ?? []);
  const [isLoading, setIsLoading] = useState(() => fetchState.data === null);
  const [error, setError] = useState<string | null>(null);

  // Refresh function that can be called after saving a new shape
  const refresh = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await listRecentShapes(10);
      fetchState.data = data;
      setShapes(data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch recent shapes:', err);
      setError('Failed to load');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Expose refresh to parent via ref
  useImperativeHandle(ref, () => ({ refresh }), [refresh]);

  useEffect(() => {
    // If we already have data, don't fetch again
    if (fetchState.data !== null) {
      return;
    }

    // If a fetch is already in progress, wait for it
    if (fetchState.promise) {
      let cancelled = false;
      fetchState.promise
        .then((data) => {
          if (!cancelled) {
            setShapes(data);
            setIsLoading(false);
          }
        })
        .catch(() => {
          if (!cancelled) {
            setError('Failed to load');
            setIsLoading(false);
          }
        });
      return () => { cancelled = true; };
    }

    // Start a new fetch
    let cancelled = false;
    fetchState.promise = listRecentShapes(10);

    fetchState.promise
      .then((data) => {
        fetchState.data = data;
        if (!cancelled) {
          setShapes(data);
          setError(null);
        }
      })
      .catch((err) => {
        console.error('Failed to fetch recent shapes:', err);
        if (!cancelled) {
          setError('Failed to load');
        }
      })
      .finally(() => {
        if (!cancelled) {
          setIsLoading(false);
        }
        fetchState.promise = null;
      });

    return () => { cancelled = true; };
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
});
