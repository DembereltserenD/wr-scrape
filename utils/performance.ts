// Performance monitoring utilities

export interface PerformanceMetrics {
  loadTime: number;
  renderTime: number;
  interactionTime: number;
  memoryUsage?: number;
}

export class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  private metrics: Map<string, PerformanceMetrics> = new Map();

  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }

  // Measure component load time
  measureLoadTime(componentName: string): () => void {
    const startTime = performance.now();

    return () => {
      const endTime = performance.now();
      const loadTime = endTime - startTime;

      this.updateMetrics(componentName, { loadTime });

      if (process.env.NODE_ENV === "development") {
        console.log(`${componentName} load time: ${loadTime.toFixed(2)}ms`);
      }
    };
  }

  // Measure render time
  measureRenderTime(componentName: string): () => void {
    const startTime = performance.now();

    return () => {
      const endTime = performance.now();
      const renderTime = endTime - startTime;

      this.updateMetrics(componentName, { renderTime });

      if (process.env.NODE_ENV === "development") {
        console.log(`${componentName} render time: ${renderTime.toFixed(2)}ms`);
      }
    };
  }

  // Measure interaction time (e.g., button clicks, form submissions)
  measureInteractionTime(actionName: string): () => void {
    const startTime = performance.now();

    return () => {
      const endTime = performance.now();
      const interactionTime = endTime - startTime;

      this.updateMetrics(actionName, { interactionTime });

      if (process.env.NODE_ENV === "development") {
        console.log(
          `${actionName} interaction time: ${interactionTime.toFixed(2)}ms`
        );
      }
    };
  }

  // Get memory usage (if available)
  getMemoryUsage(): number | undefined {
    if ("memory" in performance) {
      return (performance as any).memory.usedJSHeapSize;
    }
    return undefined;
  }

  // Update metrics for a component/action
  private updateMetrics(
    name: string,
    newMetrics: Partial<PerformanceMetrics>
  ): void {
    const existing = this.metrics.get(name) || {
      loadTime: 0,
      renderTime: 0,
      interactionTime: 0,
    };

    this.metrics.set(name, {
      ...existing,
      ...newMetrics,
      memoryUsage: this.getMemoryUsage(),
    });
  }

  // Get all metrics
  getAllMetrics(): Map<string, PerformanceMetrics> {
    return new Map(this.metrics);
  }

  // Get metrics for specific component
  getMetrics(name: string): PerformanceMetrics | undefined {
    return this.metrics.get(name);
  }

  // Clear all metrics
  clearMetrics(): void {
    this.metrics.clear();
  }

  // Log performance summary
  logSummary(): void {
    if (process.env.NODE_ENV === "development") {
      console.group("Performance Summary");
      this.metrics.forEach((metrics, name) => {
        console.log(`${name}:`, {
          loadTime: `${metrics.loadTime.toFixed(2)}ms`,
          renderTime: `${metrics.renderTime.toFixed(2)}ms`,
          interactionTime: `${metrics.interactionTime.toFixed(2)}ms`,
          memoryUsage: metrics.memoryUsage
            ? `${(metrics.memoryUsage / 1024 / 1024).toFixed(2)}MB`
            : "N/A",
        });
      });
      console.groupEnd();
    }
  }
}

// React hook for performance monitoring
export function usePerformanceMonitor(componentName: string) {
  const monitor = PerformanceMonitor.getInstance();

  const measureLoad = () => monitor.measureLoadTime(componentName);
  const measureRender = () => monitor.measureRenderTime(componentName);
  const measureInteraction = (actionName: string) =>
    monitor.measureInteractionTime(`${componentName}.${actionName}`);

  return {
    measureLoad,
    measureRender,
    measureInteraction,
    getMetrics: () => monitor.getMetrics(componentName),
  };
}

// Web Vitals monitoring
export function measureWebVitals() {
  if (typeof window !== "undefined") {
    // Measure Largest Contentful Paint (LCP)
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const lastEntry = entries[entries.length - 1];
      console.log("LCP:", lastEntry.startTime);
    }).observe({ entryTypes: ["largest-contentful-paint"] });

    // Measure First Input Delay (FID)
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry: any) => {
        if (entry.processingStart && entry.startTime) {
          console.log("FID:", entry.processingStart - entry.startTime);
        }
      });
    }).observe({ entryTypes: ["first-input"] });

    // Measure Cumulative Layout Shift (CLS)
    let clsValue = 0;
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry: any) => {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
        }
      });
      console.log("CLS:", clsValue);
    }).observe({ entryTypes: ["layout-shift"] });
  }
}

// Image loading optimization
export function preloadImage(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve();
    img.onerror = reject;
    img.src = src;
  });
}

// Lazy loading utility
export function createIntersectionObserver(
  callback: (entries: IntersectionObserverEntry[]) => void,
  options?: IntersectionObserverInit
): IntersectionObserver | null {
  if (typeof window !== "undefined" && "IntersectionObserver" in window) {
    return new IntersectionObserver(callback, {
      rootMargin: "50px",
      threshold: 0.1,
      ...options,
    });
  }
  return null;
}
