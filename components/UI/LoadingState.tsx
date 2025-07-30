import React from 'react';
import LoadingSpinner from './LoadingSpinner';

interface LoadingStateProps {
    message?: string;
    size?: 'sm' | 'md' | 'lg';
    className?: string;
    showSkeleton?: boolean;
    type?: 'spinner' | 'skeleton' | 'pulse';
}

const LoadingState: React.FC<LoadingStateProps> = ({
    message = 'Loading...',
    size = 'md',
    className = '',
    showSkeleton = false,
    type = 'spinner'
}) => {
    if (type === 'skeleton') {
        return (
            <div className={`animate-pulse ${className}`}>
                <div className="bg-card-background rounded-xl p-6 space-y-4">
                    <div className="h-48 bg-gray-300 dark:bg-gray-600 rounded-lg"></div>
                    <div className="space-y-2">
                        <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-3/4"></div>
                        <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-1/2"></div>
                    </div>
                </div>
            </div>
        );
    }

    if (type === 'pulse') {
        return (
            <div className={`flex items-center justify-center p-8 ${className}`}>
                <div className="flex space-x-2">
                    <div className="w-3 h-3 bg-primary-purple rounded-full animate-pulse"></div>
                    <div className="w-3 h-3 bg-primary-purple rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-3 h-3 bg-primary-purple rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                </div>
                {message && (
                    <p className="text-text-secondary text-center ml-4">{message}</p>
                )}
            </div>
        );
    }

    return (
        <div className={`flex flex-col items-center justify-center p-8 transition-opacity duration-300 ${className}`}>
            <LoadingSpinner size={size} color="primary" className="mb-4" />
            <p className="text-text-secondary text-center animate-pulse">{message}</p>
        </div>
    );
};

export default LoadingState;