import React, { useState, useRef, useEffect } from "react";

interface TooltipProps {
  children: React.ReactNode;
  content: React.ReactNode;
  className?: string;
  delay?: number;
}

const Tooltip: React.FC<TooltipProps> = ({
  children,
  content,
  className = "",
  delay = 300,
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const triggerRef = useRef<HTMLDivElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const showTooltip = (e: React.MouseEvent) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      const rect = triggerRef.current?.getBoundingClientRect();
      if (rect) {
        // Position tooltip closer to the image
        const x = rect.left + rect.width / 2;
        const y = rect.top - 5; // Reduced gap from 10 to 5
        setPosition({ x, y });
        setIsVisible(true);
      }
    }, delay);
  };

  const hideTooltip = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
  };

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (isVisible && tooltipRef.current) {
      const tooltip = tooltipRef.current;
      const rect = tooltip.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      let adjustedX = position.x - rect.width / 2;
      let adjustedY = position.y - rect.height;

      // Adjust horizontal position if tooltip goes off screen
      if (adjustedX < 10) {
        adjustedX = 10;
      } else if (adjustedX + rect.width > viewportWidth - 10) {
        adjustedX = viewportWidth - rect.width - 10;
      }

      // Adjust vertical position if tooltip goes off screen
      if (adjustedY < 10) {
        const triggerRect = triggerRef.current?.getBoundingClientRect();
        if (triggerRect) {
          adjustedY = triggerRect.bottom + 5; // Show below the trigger element
        } else {
          adjustedY = position.y + 40; // Fallback
        }
      }

      tooltip.style.left = `${adjustedX}px`;
      tooltip.style.top = `${adjustedY}px`;
    }
  }, [isVisible, position]);

  return (
    <>
      <div
        ref={triggerRef}
        onMouseEnter={showTooltip}
        onMouseLeave={hideTooltip}
        className={`inline-block ${className}`}
      >
        {children}
      </div>

      {isVisible && (
        <div
          ref={tooltipRef}
          className="fixed z-[9999] pointer-events-none"
          style={{
            left: position.x,
            top: position.y,
          }}
        >
          <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 border-2 border-yellow-400/60 rounded-lg shadow-2xl backdrop-blur-sm max-w-sm">
            <div className="p-4">{content}</div>
            {/* Arrow */}
            <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
              <div className="w-4 h-4 bg-slate-900 border-r-2 border-b-2 border-yellow-400/60 transform rotate-45"></div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Tooltip;
export type { TooltipProps };
