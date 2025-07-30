// Accessibility utilities and testing helpers

export interface AccessibilityIssue {
  element: Element;
  issue: string;
  severity: "error" | "warning" | "info";
  suggestion: string;
}

export class AccessibilityChecker {
  private issues: AccessibilityIssue[] = [];

  // Check for missing alt text on images
  checkImageAltText(): AccessibilityIssue[] {
    const images = document.querySelectorAll("img");
    const issues: AccessibilityIssue[] = [];

    images.forEach((img) => {
      if (!img.alt && !img.getAttribute("aria-label")) {
        issues.push({
          element: img,
          issue: "Missing alt text",
          severity: "error",
          suggestion: "Add descriptive alt text or aria-label to the image",
        });
      } else if (img.alt && img.alt.length < 3) {
        issues.push({
          element: img,
          issue: "Alt text too short",
          severity: "warning",
          suggestion: "Provide more descriptive alt text",
        });
      }
    });

    return issues;
  }

  // Check for proper heading hierarchy
  checkHeadingHierarchy(): AccessibilityIssue[] {
    const headings = document.querySelectorAll("h1, h2, h3, h4, h5, h6");
    const issues: AccessibilityIssue[] = [];
    let previousLevel = 0;

    headings.forEach((heading) => {
      const currentLevel = parseInt(heading.tagName.charAt(1));

      if (currentLevel > previousLevel + 1) {
        issues.push({
          element: heading,
          issue: "Heading hierarchy skipped",
          severity: "warning",
          suggestion: `Use h${
            previousLevel + 1
          } instead of h${currentLevel} to maintain proper hierarchy`,
        });
      }

      previousLevel = currentLevel;
    });

    return issues;
  }

  // Check for keyboard accessibility
  checkKeyboardAccessibility(): AccessibilityIssue[] {
    const interactiveElements = document.querySelectorAll(
      'button, a, input, select, textarea, [tabindex], [role="button"], [role="link"]'
    );
    const issues: AccessibilityIssue[] = [];

    interactiveElements.forEach((element) => {
      const tabIndex = element.getAttribute("tabindex");

      // Check for positive tabindex (anti-pattern)
      if (tabIndex && parseInt(tabIndex) > 0) {
        issues.push({
          element,
          issue: "Positive tabindex found",
          severity: "warning",
          suggestion:
            'Use tabindex="0" or remove tabindex to maintain natural tab order',
        });
      }

      // Check for missing focus indicators
      const computedStyle = window.getComputedStyle(element, ":focus");
      if (
        computedStyle.outline === "none" &&
        !computedStyle.boxShadow.includes("ring")
      ) {
        issues.push({
          element,
          issue: "Missing focus indicator",
          severity: "error",
          suggestion: "Add visible focus styles for keyboard navigation",
        });
      }
    });

    return issues;
  }

  // Check for color contrast
  checkColorContrast(): AccessibilityIssue[] {
    const textElements = document.querySelectorAll(
      "p, span, div, h1, h2, h3, h4, h5, h6, a, button"
    );
    const issues: AccessibilityIssue[] = [];

    textElements.forEach((element) => {
      const style = window.getComputedStyle(element);
      const color = style.color;
      const backgroundColor = style.backgroundColor;

      // Simple contrast check (would need more sophisticated implementation for production)
      if (color === backgroundColor) {
        issues.push({
          element,
          issue: "Poor color contrast",
          severity: "error",
          suggestion:
            "Ensure sufficient color contrast between text and background",
        });
      }
    });

    return issues;
  }

  // Check for ARIA labels and roles
  checkAriaLabels(): AccessibilityIssue[] {
    const elementsNeedingLabels = document.querySelectorAll(
      "button:not([aria-label]):not([aria-labelledby]), input:not([aria-label]):not([aria-labelledby]):not([id])"
    );
    const issues: AccessibilityIssue[] = [];

    elementsNeedingLabels.forEach((element) => {
      if (element.tagName === "BUTTON" && !element.textContent?.trim()) {
        issues.push({
          element,
          issue: "Button without accessible name",
          severity: "error",
          suggestion:
            "Add aria-label, aria-labelledby, or text content to the button",
        });
      }

      if (
        element.tagName === "INPUT" &&
        !element.previousElementSibling?.tagName.includes("LABEL")
      ) {
        issues.push({
          element,
          issue: "Input without label",
          severity: "error",
          suggestion: "Add a label element or aria-label to the input",
        });
      }
    });

    return issues;
  }

  // Run all accessibility checks
  runAllChecks(): AccessibilityIssue[] {
    this.issues = [
      ...this.checkImageAltText(),
      ...this.checkHeadingHierarchy(),
      ...this.checkKeyboardAccessibility(),
      ...this.checkColorContrast(),
      ...this.checkAriaLabels(),
    ];

    return this.issues;
  }

  // Get issues by severity
  getIssuesBySeverity(
    severity: "error" | "warning" | "info"
  ): AccessibilityIssue[] {
    return this.issues.filter((issue) => issue.severity === severity);
  }

  // Log accessibility report
  logReport(): void {
    if (process.env.NODE_ENV === "development") {
      const errors = this.getIssuesBySeverity("error");
      const warnings = this.getIssuesBySeverity("warning");
      const info = this.getIssuesBySeverity("info");

      console.group("Accessibility Report");

      if (errors.length > 0) {
        console.group(`❌ Errors (${errors.length})`);
        errors.forEach((issue) => {
          console.error(issue.issue, issue.element, issue.suggestion);
        });
        console.groupEnd();
      }

      if (warnings.length > 0) {
        console.group(`⚠️ Warnings (${warnings.length})`);
        warnings.forEach((issue) => {
          console.warn(issue.issue, issue.element, issue.suggestion);
        });
        console.groupEnd();
      }

      if (info.length > 0) {
        console.group(`ℹ️ Info (${info.length})`);
        info.forEach((issue) => {
          console.info(issue.issue, issue.element, issue.suggestion);
        });
        console.groupEnd();
      }

      if (errors.length === 0 && warnings.length === 0 && info.length === 0) {
        console.log("✅ No accessibility issues found!");
      }

      console.groupEnd();
    }
  }
}

// Keyboard navigation helpers
export const KeyboardNavigation = {
  // Trap focus within an element
  trapFocus(element: HTMLElement): () => void {
    const focusableElements = element.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    ) as NodeListOf<HTMLElement>;

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Tab") {
        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }
    };

    element.addEventListener("keydown", handleKeyDown);

    // Return cleanup function
    return () => {
      element.removeEventListener("keydown", handleKeyDown);
    };
  },

  // Handle escape key
  handleEscape(callback: () => void): () => void {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        callback();
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  },

  // Announce to screen readers
  announce(message: string, priority: "polite" | "assertive" = "polite"): void {
    const announcer = document.createElement("div");
    announcer.setAttribute("aria-live", priority);
    announcer.setAttribute("aria-atomic", "true");
    announcer.className = "sr-only";
    announcer.textContent = message;

    document.body.appendChild(announcer);

    setTimeout(() => {
      document.body.removeChild(announcer);
    }, 1000);
  },
};

// Screen reader utilities
export const ScreenReader = {
  // Check if screen reader is active
  isActive(): boolean {
    return (
      window.navigator.userAgent.includes("NVDA") ||
      window.navigator.userAgent.includes("JAWS") ||
      window.speechSynthesis?.speaking ||
      false
    );
  },

  // Announce page changes
  announcePageChange(title: string): void {
    KeyboardNavigation.announce(`Page changed to ${title}`, "assertive");
  },

  // Announce loading states
  announceLoading(isLoading: boolean, context?: string): void {
    const message = isLoading
      ? `Loading${context ? ` ${context}` : ""}...`
      : `Finished loading${context ? ` ${context}` : ""}`;

    KeyboardNavigation.announce(message, "polite");
  },
};

// React hook for accessibility
export function useAccessibility() {
  const checker = new AccessibilityChecker();

  const runAccessibilityCheck = () => {
    const issues = checker.runAllChecks();
    checker.logReport();
    return issues;
  };

  const announceToScreenReader = (
    message: string,
    priority?: "polite" | "assertive"
  ) => {
    KeyboardNavigation.announce(message, priority);
  };

  const trapFocus = (element: HTMLElement) => {
    return KeyboardNavigation.trapFocus(element);
  };

  return {
    runAccessibilityCheck,
    announceToScreenReader,
    trapFocus,
    isScreenReaderActive: ScreenReader.isActive,
  };
}
