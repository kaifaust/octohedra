'use client';

import { ReactNode } from 'react';
import { ChevronUp, ChevronDown, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface MobileBottomSheetProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  headerActions?: ReactNode;
  children: ReactNode;
}

export function MobileBottomSheet({
  isOpen,
  onOpenChange,
  title,
  headerActions,
  children,
}: MobileBottomSheetProps) {
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
        className={`fixed bottom-0 left-0 right-0 z-50 transition-transform duration-300 ease-out ${
          isOpen ? 'translate-y-0' : 'translate-y-[calc(100%-3.5rem)]'
        }`}
      >
        {/* Pull Tab / Header - always visible */}
        <div
          className="bg-card/95 backdrop-blur-md border-t border-x border-border/50 rounded-t-2xl shadow-lg cursor-pointer"
          onClick={() => onOpenChange(!isOpen)}
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
            <div className="flex items-center gap-2">
              {headerActions}
              {isOpen && (
                <Button
                  variant="ghost"
                  size="icon-sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    onOpenChange(false);
                  }}
                  className="h-8 w-8 text-muted-foreground hover:text-foreground"
                >
                  <X className="h-4 w-4" />
                </Button>
              )}
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
