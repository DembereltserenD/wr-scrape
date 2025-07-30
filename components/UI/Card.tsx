import React, { forwardRef } from 'react';

export type CardVariant = 'default' | 'elevated' | 'outlined' | 'gaming';
export type CardSize = 'sm' | 'md' | 'lg';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: CardVariant;
    size?: CardSize;
    hoverable?: boolean;
    clickable?: boolean;
    loading?: boolean;
    children: React.ReactNode;
}

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
    children: React.ReactNode;
}

export interface CardBodyProps extends React.HTMLAttributes<HTMLDivElement> {
    children: React.ReactNode;
}

export interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {
    children: React.ReactNode;
}

const Card = forwardRef<HTMLDivElement, CardProps>(({
    variant = 'default',
    size = 'md',
    hoverable = false,
    clickable = false,
    loading = false,
    className = '',
    children,
    ...props
}, ref) => {
    if (loading) {
        return (
            <div ref={ref} className={className} {...props}>
                <div>
                    <div></div>
                    <div></div>
                    <div></div>
                </div>
            </div>
        );
    }

    return (
        <div
            ref={ref}
            className={className}
            role={clickable ? 'button' : undefined}
            tabIndex={clickable ? 0 : undefined}
            {...props}
        >
            {children}
        </div>
    );
});

const CardHeader = forwardRef<HTMLDivElement, CardHeaderProps>(({
    className = '',
    children,
    ...props
}, ref) => {
    return (
        <div ref={ref} className={className} {...props}>
            {children}
        </div>
    );
});

const CardBody = forwardRef<HTMLDivElement, CardBodyProps>(({
    className = '',
    children,
    ...props
}, ref) => {
    return (
        <div ref={ref} className={className} {...props}>
            {children}
        </div>
    );
});

const CardFooter = forwardRef<HTMLDivElement, CardFooterProps>(({
    className = '',
    children,
    ...props
}, ref) => {
    return (
        <div ref={ref} className={className} {...props}>
            {children}
        </div>
    );
});

Card.displayName = 'Card';
CardHeader.displayName = 'CardHeader';
CardBody.displayName = 'CardBody';
CardFooter.displayName = 'CardFooter';

export { Card as default, CardHeader, CardBody, CardFooter };