import React, { useState, useRef, useEffect, forwardRef } from "react";

export interface DropdownOption {
  value: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
}

export type DropdownVariant = "default" | "gaming" | "minimal";
export type DropdownSize = "sm" | "md" | "lg";

export interface DropdownProps {
  options: DropdownOption[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  className?: string;
  disabled?: boolean;
  variant?: DropdownVariant;
  size?: DropdownSize;
  searchable?: boolean;
  loading?: boolean;
  error?: string;
  label?: string;
  required?: boolean;
}

const Dropdown = forwardRef<HTMLDivElement, DropdownProps>(
  (
    {
      options,
      value,
      onChange,
      placeholder = "Select an option",
      className = "",
      disabled = false,
      variant = "default",
      size = "md",
      searchable = false,
      loading = false,
      error,
      label,
      required = false,
    },
    ref,
  ) => {
    const [isOpen, setIsOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [focusedIndex, setFocusedIndex] = useState(-1);
    const dropdownRef = useRef<HTMLDivElement>(null);
    const searchInputRef = useRef<HTMLInputElement>(null);

    // Filter options based on search term
    const filteredOptions = searchable
      ? options.filter((option) =>
          option.label.toLowerCase().includes(searchTerm.toLowerCase()),
        )
      : options;

    // Close dropdown when clicking outside
    useEffect(() => {
      const handleClickOutside = (event: MouseEvent) => {
        if (
          dropdownRef.current &&
          !dropdownRef.current.contains(event.target as Node)
        ) {
          setIsOpen(false);
          setSearchTerm("");
          setFocusedIndex(-1);
        }
      };

      document.addEventListener("mousedown", handleClickOutside);
      return () => {
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }, []);

    // Handle keyboard navigation
    useEffect(() => {
      const handleKeyDown = (event: KeyboardEvent) => {
        if (!isOpen) return;

        switch (event.key) {
          case "Escape":
            setIsOpen(false);
            setSearchTerm("");
            setFocusedIndex(-1);
            break;
          case "ArrowDown":
            event.preventDefault();
            setFocusedIndex((prev) =>
              prev < filteredOptions.length - 1 ? prev + 1 : 0,
            );
            break;
          case "ArrowUp":
            event.preventDefault();
            setFocusedIndex((prev) =>
              prev > 0 ? prev - 1 : filteredOptions.length - 1,
            );
            break;
          case "Enter":
            event.preventDefault();
            if (focusedIndex >= 0 && filteredOptions[focusedIndex]) {
              handleOptionClick(filteredOptions[focusedIndex].value);
            }
            break;
        }
      };

      document.addEventListener("keydown", handleKeyDown);
      return () => {
        document.removeEventListener("keydown", handleKeyDown);
      };
    }, [isOpen, focusedIndex, filteredOptions]);

    // Focus search input when dropdown opens
    useEffect(() => {
      if (isOpen && searchable && searchInputRef.current) {
        searchInputRef.current.focus();
      }
    }, [isOpen, searchable]);

    const selectedOption = options.find((option) => option.value === value);

    const handleOptionClick = (optionValue: string) => {
      const option = options.find((opt) => opt.value === optionValue);
      if (option && !option.disabled) {
        onChange(optionValue);
        setIsOpen(false);
        setSearchTerm("");
        setFocusedIndex(-1);
      }
    };

    const handleToggle = () => {
      if (!disabled) {
        setIsOpen(!isOpen);
        if (!isOpen) {
          setFocusedIndex(-1);
        }
      }
    };

    return (
      <div className={className} ref={ref || dropdownRef}>
        {label && (
          <label className="block text-sm font-medium text-gray-300 mb-2">
            {label}
            {required && <span className="text-red-400 ml-1">*</span>}
          </label>
        )}

        <button
          type="button"
          onClick={handleToggle}
          disabled={disabled || loading}
          aria-haspopup="listbox"
          aria-expanded={isOpen}
          aria-label={label || placeholder}
          aria-required={required}
          aria-invalid={!!error}
          className={`
            relative w-full px-4 py-3 text-left bg-slate-800/50 backdrop-blur-sm border border-slate-600/50 rounded-lg
            transition-all duration-200 ease-in-out
            hover:bg-slate-700/50 hover:border-slate-500/50 hover:shadow-lg hover:shadow-blue-500/10
            focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50
            disabled:opacity-50 disabled:cursor-not-allowed
            ${isOpen ? "ring-2 ring-blue-500/50 border-blue-500/50 bg-slate-700/50" : ""}
            ${error ? "border-red-500/50 ring-1 ring-red-500/50" : ""}
            ${variant === "gaming" ? "bg-gradient-to-r from-blue-900/20 to-purple-900/20 border-blue-500/30" : ""}
            ${size === "sm" ? "px-3 py-2 text-sm" : size === "lg" ? "px-5 py-4 text-lg" : "px-4 py-3"}
          `}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              {loading ? (
                <svg
                  className="w-5 h-5 animate-spin text-blue-400"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="2"
                    className="opacity-25"
                  />
                  <path
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    className="opacity-75"
                  />
                </svg>
              ) : (
                selectedOption?.icon && (
                  <span className="flex-shrink-0 text-blue-400">
                    {selectedOption.icon}
                  </span>
                )
              )}
              <span
                className={`block truncate font-medium ${
                  selectedOption ? "text-white" : "text-gray-400"
                }`}
              >
                {selectedOption ? selectedOption.label : placeholder}
              </span>
            </div>
            <svg
              className={`w-5 h-5 text-gray-400 transition-transform duration-200 ${
                isOpen ? "rotate-180" : ""
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </div>
        </button>
        {error && <p className="mt-2 text-sm text-red-400">{error}</p>}

        {isOpen && (
          <div className="absolute z-50 w-full mt-2 bg-slate-800/95 backdrop-blur-sm border border-slate-600/50 rounded-lg shadow-2xl shadow-black/50 max-h-60 overflow-hidden">
            {searchable && (
              <div className="p-3 border-b border-slate-600/50">
                <label htmlFor="dropdown-search" className="sr-only">
                  Search options
                </label>
                <input
                  id="dropdown-search"
                  ref={searchInputRef}
                  type="text"
                  placeholder="Search options..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  aria-label="Search options"
                  className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600/50 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50"
                />
              </div>
            )}

            <div className="max-h-48 overflow-y-auto">
              <ul role="listbox" className="py-1">
                {filteredOptions.length === 0 ? (
                  <li className="px-4 py-3 text-gray-400 text-center">
                    No options found
                  </li>
                ) : (
                  filteredOptions.map((option, index) => (
                    <li
                      key={option.value}
                      onClick={() => handleOptionClick(option.value)}
                      role="option"
                      aria-selected={value === option.value}
                      aria-disabled={option.disabled}
                      className={`
                        px-4 py-3 cursor-pointer transition-all duration-150
                        hover:bg-slate-700/50 hover:text-white
                        ${focusedIndex === index ? "bg-slate-700/50 text-white" : "text-gray-300"}
                        ${value === option.value ? "bg-blue-600/20 text-blue-300" : ""}
                        ${option.disabled ? "opacity-50 cursor-not-allowed" : ""}
                      `}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          {option.icon && (
                            <span className="flex-shrink-0 text-blue-400">
                              {option.icon}
                            </span>
                          )}
                          <span className="font-medium">{option.label}</span>
                        </div>
                        {value === option.value && (
                          <svg
                            className="w-5 h-5 text-blue-400"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                          >
                            <path
                              fillRule="evenodd"
                              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                              clipRule="evenodd"
                            />
                          </svg>
                        )}
                      </div>
                    </li>
                  ))
                )}
              </ul>
            </div>
          </div>
        )}
      </div>
    );
  },
);

Dropdown.displayName = "Dropdown";

export default Dropdown;
