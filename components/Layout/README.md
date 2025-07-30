# Layout Components

This directory contains layout components for the Wild Rift homepage.

## Header Component

The Header component provides a responsive navigation header with the following features:

### Features

1. **Responsive Design**

   - Desktop navigation with horizontal menu
   - Mobile hamburger menu with slide-down navigation
   - Responsive breakpoints using Tailwind CSS

2. **Navigation Items**

   - Home
   - Champion
   - Tier List
   - Items
   - Comment

3. **Language Switching**

   - Integrated LanguageSwitcher component
   - Supports Mongolian (mn) and English (en)
   - Dropdown interface with flags and language names

4. **Visual Effects**

   - Scroll-based header styling (background blur and shadow)
   - Smooth transitions and animations
   - Active route highlighting
   - Hover effects

5. **Dark Theme**
   - Uses custom purple color scheme
   - Gradient logo design
   - Proper contrast for accessibility

### Usage

```tsx
import { Layout } from "../components/Layout";

const MyPage = () => {
  return <Layout currentPage="/current-route">{/* Page content */}</Layout>;
};
```

### Props

#### Header Component

- `currentPage?: string` - Optional current page path for active state highlighting

#### Layout Component

- `children: ReactNode` - Page content to render
- `currentPage?: string` - Optional current page path passed to Header

### Styling

The header uses Tailwind CSS with custom color variables defined in `tailwind.config.js`:

- `primary-purple`: Main brand color
- `dark-purple`: Header background
- `text-primary`: Primary text color (white)
- `text-secondary`: Secondary text color (light purple)
- `card-background`: Background for dropdowns and cards

### Mobile Responsiveness

- Hamburger menu appears on screens smaller than `md` (768px)
- Mobile menu slides down with smooth animation
- Language switcher adapts to mobile layout
- Touch-friendly button sizes

### Accessibility

- Proper ARIA labels for mobile menu button
- Keyboard navigation support
- High contrast colors
- Focus states for interactive elements

## Layout Component

The Layout component wraps the Header and provides a consistent page structure:

- Sets minimum height to full screen
- Applies dark background theme
- Positions header as sticky at top
- Provides main content area

### File Structure

```
components/Layout/
├── Header.tsx          # Main header component
├── Layout.tsx          # Layout wrapper component
├── index.ts           # Export barrel
└── README.md          # This documentation
```

### Dependencies

- Next.js (Link, useRouter)
- React (useState, useEffect)
- LanguageContext (useLanguage hook)
- LanguageSwitcher component
- Tailwind CSS for styling
