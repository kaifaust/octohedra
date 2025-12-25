'use client';

import { ReactNode, useRef, useState } from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';

interface MobileBottomSheetProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  headerActions?: ReactNode;
  children: ReactNode;
}

const DRAG_THRESHOLD = 50; // pixels needed to trigger open/close

export function MobileBottomSheet({
  isOpen,
  onOpenChange,
  title,
  headerActions,
  children,
}: MobileBottomSheetProps) {
  const [dragOffset, setDragOffset] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const dragStartY = useRef(0);
  const sheetRef = useRef<HTMLDivElement>(null);

  const handleTouchStart = (e: React.TouchEvent) => {
    dragStartY.current = e.touches[0].clientY;
    setIsDragging(true);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging) return;

    const currentY = e.touches[0].clientY;
    const delta = currentY - dragStartY.current;

    if (isOpen) {
      // When open, only allow dragging down (positive delta)
      setDragOffset(Math.max(0, delta));
    } else {
      // When closed, only allow dragging up (negative delta)
      setDragOffset(Math.min(0, delta));
    }
  };

  const handleTouchEnd = () => {
    setIsDragging(false);

    if (isOpen && dragOffset > DRAG_THRESHOLD) {
      // Dragged down enough to close
      onOpenChange(false);
    } else if (!isOpen && dragOffset < -DRAG_THRESHOLD) {
      // Dragged up enough to open
      onOpenChange(true);
    }

    setDragOffset(0);
  };

  const handleHeaderClick = () => {
    if (!isDragging || Math.abs(dragOffset) < 5) {
      onOpenChange(!isOpen);
    }
  };

  // Calculate transform based on open state and drag offset
  const getTransform = () => {
    if (isDragging) {
      if (isOpen) {
        return `translateY(${dragOffset}px)`;
      } else {
        return `translateY(calc(100% - 3.5rem + ${dragOffset}px))`;
      }
    }
    return isOpen ? 'translateY(0)' : 'translateY(calc(100% - 3.5rem))';
  };

  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/20 z-40 transition-opacity"
          onClick={() => onOpenChange(false)}
        />
      )}

      {/* Bottom Sheet */}
      <div
        ref={sheetRef}
        className="fixed bottom-0 left-0 right-0 z-40 select-none"
        style={{
          transform: getTransform(),
          transition: isDragging ? 'none' : 'transform 300ms ease-out',
        }}
      >
        {/* Pull Tab / Header - always visible */}
        <div
          className="bg-card/95 backdrop-blur-md border-t border-x border-border/50 rounded-t-2xl shadow-lg cursor-grab active:cursor-grabbing touch-none"
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
          onClick={handleHeaderClick}
        >
          {/* Handle bar */}
          <div className="flex justify-center py-2">
            <div className="w-10 h-1 bg-muted-foreground/30 rounded-full" />
          </div>

          {/* Header */}
          <div className="flex items-center justify-between px-4 pb-3">
            <div className="flex items-center gap-2">
              {isOpen ? (
                <ChevronDown className="h-5 w-5 text-muted-foreground" />
              ) : (
                <ChevronUp className="h-5 w-5 text-muted-foreground" />
              )}
              <h2 className="text-lg font-semibold">{title}</h2>
            </div>
            <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
              {headerActions}
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="bg-card/95 backdrop-blur-md border-x border-border/50 overflow-y-auto max-h-[70vh]">
          <div className="px-4 pb-8 pt-2">
            {children}
          </div>
        </div>
      </div>
    </>
  );
}
