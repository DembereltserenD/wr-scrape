import React, { useState, useRef, useEffect, forwardRef } from 'react';

export interface DropdownOption {
    value: string;
    label: string;
    icon?: React.ReactNode;
    disabled?: boolean;
}

export type DropdownVariant = 'default' | 'gaming' | 'minimal';
export type DropdownSize = 'sm' | 'md' | 'lg';

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

const Dropdown = forwardRef<HTMLDivElement, DropdownProps>(({
    options,
    value,
    onChange,
    placeholder = 'Select an option',
    className = '',
    disabled = false,
    variant = 'default',
    size = 'md',
    searchable = false,
    loading = false,
    error,
    label,
    required = false
}, ref) => {
    const [isOpen, setIsOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [focusedIndex, setFocusedIndex] = useState(-1);
    const dropdownRef = useRef<HTMLDivElement>(null);
    const searchInputRef = useRef<HTMLInputElement>(null);

    // Filter options based on search term
    const filteredOptions = searchable
        ? options.filter(option =>
            option.label.toLowerCase().includes(searchTerm.toLowerCase())
        )
        : options; /
            / Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
                setSearchTerm('');
                setFocusedIndex(-1);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    // Handle keyboard navigation
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (!isOpen) return;

            switch (event.key) {
                case 'Escape':
                    setIsOpen(false);
                    setSearchTerm('');
                    setFocusedIndex(-1);
                    break;
                case 'ArrowDown':
                    event.preventDefault();
                    setFocusedIndex(prev =>
                        prev < filteredOptions.length - 1 ? prev + 1 : 0
                    );
                    break;
                case 'ArrowUp':
                    event.preventDefault();
                    setFocusedIndex(prev =>
                        prev > 0 ? prev - 1 : filteredOptions.length - 1
                    );
                    break;
                case 'Enter':
                    event.preventDefault();
                    if (focusedIndex >= 0 && filteredOptions[focusedIndex]) {
                        handleOptionClick(filteredOptions[focusedIndex].value);
                    }
                    break;
            }
        };

        document.addEventListener('keydown', handleKeyDown);
        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [isOpen, focusedIndex, filteredOptions]);

    // Focus search input when dropdown opens
    useEffect(() => {
        if (isOpen && searchable && searchInputRef.current) {
            searchInputRef.current.focus();
        }
    }, [isOpen, searchable]);

    const selectedOption = options.find(option => option.value === value); co
nst handleOptionClick = (optionValue: string) => {
        const option = options.find(opt => opt.value === optionValue);
        if (option && !option.disabled) {
            onChange(optionValue);
            setIsOpen(false);
            setSearchTerm('');
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
                <label>
                    {label}
                    {required && <span>*</span>}
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
            >
                <div>
                    <div>
                        {loading ? (
                            <svg fill="none" viewBox="0 0 24 24">
                                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                            </svg>
                        ) : selectedOption?.icon && (
                            <span>
                                {selectedOption.icon}
                            </span>
                        )}
                        <span>
                            {selectedOption ? selectedOption.label : placeholder}
                        </span>
                    </div>
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                </div>
            </button>
            {error && (
                <p>{error}</p>
            )}

            {isOpen && (
                <div>
                    {searchable && (
                        <div>
                            <label htmlFor="dropdown-search">Search options</label>
                            <input
                                id="dropdown-search"
                                ref={searchInputRef}
                                type="text"
                                placeholder="Search options..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                aria-label="Search options"
                            />
                        </div>
                    )}

                    <div>
                        <ul role="listbox">
                            {filteredOptions.length === 0 ? (
                                <li>
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
                                    >
                                        <div>
                                            <div>
                                                {option.icon && (
                                                    <span>
                                                        {option.icon}
                                                    </span>
                                                )}
                                                <span>{option.label}</span>
                                            </div>
                                            {value === option.value && (
                                                <svg fill="currentColor" viewBox="0 0 20 20">
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
});

Dropdown.displayName = 'Dropdown';

export default Dropdown;