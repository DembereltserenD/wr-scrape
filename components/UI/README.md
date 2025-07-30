# UI Components

This directory contains reusable UI components for the Wild Rift homepage with a gaming theme.

## Components

### Button

A versatile button component with gaming theme and hover effects.

**Props:**

- `variant`: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
- `size`: 'sm' | 'md' | 'lg' | 'xl'
- `loading`: boolean - Shows loading spinner
- `leftIcon`: React.ReactNode - Icon on the left side
- `rightIcon`: React.ReactNode - Icon on the right side
- `fullWidth`: boolean - Makes button full width
- `disabled`: boolean - Disables the button

**Features:**

- Gaming-themed gradient backgrounds
- Hover effects with glow and scale animations
- Loading state with spinner
- Keyboard navigation support
- Accessibility compliant

**Example:**

```tsx
<Button variant="primary" size="lg" leftIcon={<PlusIcon />}>
  Add Champion
</Button>
```

### Card

A flexible card component for displaying content with gaming aesthetics.

**Props:**

- `variant`: 'default' | 'elevated' | 'outlined' | 'gaming'
- `size`: 'sm' | 'md' | 'lg'
- `hoverable`: boolean - Adds hover effects
- `clickable`: boolean - Makes card clickable with focus states
- `loading`: boolean - Shows loading skeleton

**Sub-components:**

- `CardHeader`: Header section of the card
- `CardBody`: Main content area
- `CardFooter`: Footer section with border separator

**Features:**

- Gaming variant with gradient backgrounds and glow effects
- Hover animations (lift and shadow)
- Loading skeleton state
- Responsive sizing
- Accessibility support for clickable cards

**Example:**

```tsx
<Card variant="gaming" hoverable>
  <CardHeader>
    <h3>Champion Name</h3>
  </CardHeader>
  <CardBody>
    <p>Champion description</p>
  </CardBody>
  <CardFooter>
    <Button variant="primary">View Details</Button>
  </CardFooter>
</Card>
```

### Dropdown

An enhanced dropdown component with gaming theme and advanced features.

**Props:**

- `options`: DropdownOption[] - Array of options
- `value`: string - Selected value
- `onChange`: (value: string) => void - Change handler
- `variant`: 'default' | 'gaming' | 'minimal'
- `size`: 'sm' | 'md' | 'lg'
- `searchable`: boolean - Enables search functionality
- `loading`: boolean - Shows loading state
- `disabled`: boolean - Disables the dropdown
- `error`: string - Error message
- `label`: string - Label text
- `required`: boolean - Marks as required field

**DropdownOption Interface:**

```tsx
interface DropdownOption {
  value: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
}
```

**Features:**

- Gaming variant with gradient backgrounds and glow effects
- Keyboard navigation (Arrow keys, Enter, Escape)
- Search functionality with filtering
- Icons support in options
- Loading and error states
- Accessibility compliant with ARIA attributes
- Click outside to close
- Focus management

**Example:**

```tsx
<Dropdown
  variant="gaming"
  searchable
  options={[
    { value: "strongest", label: "Хамгийн хүчтэй", icon: <StarIcon /> },
    { value: "strong", label: "Хүчтэй" },
    { value: "good", label: "Сайн" },
  ]}
  value={selectedTier}
  onChange={setSelectedTier}
  placeholder="Select tier..."
  label="Champion Tier"
/>
```

## Gaming Theme Features

All components include:

- Dark purple color scheme matching the site theme
- Gradient backgrounds and hover effects
- Glow animations on hover
- Smooth transitions and animations
- Responsive design for all screen sizes
- Accessibility compliance
- Keyboard navigation support

## Testing

Visit `/ui-components-test` to see all components in action with various configurations and states.

## Accessibility

All components follow WCAG guidelines:

- Proper ARIA attributes
- Keyboard navigation
- Focus management
- Screen reader support
- Sufficient color contrast
- Touch-friendly sizing on mobile devices
