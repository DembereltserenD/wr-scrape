import React, { useState, useRef, useEffect } from "react";

interface LazyImageProps {
    src: string;
    alt: string;
    className?: string;
    placeholder?: string;
    onError?: (e: React.SyntheticEvent<HTMLImageElement, Event>) => void;
}

const LazyImage: React.FC<LazyImageProps> = ({
    src,
    alt,
    className = "",
    placeholder = "/placeholder-champion.svg",
    onError,
}) => {
    const [isLoaded, setIsLoaded] = useState(false);
    const [isInView, setIsInView] = useState(false);
    const [hasError, setHasError] = useState(false);
    const imgRef = useRef<HTMLImageElement>(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsInView(true);
                    observer.disconnect();
                }
            },
            { threshold: 0.1 }
        );

        if (imgRef.current) {
            observer.observe(imgRef.current);
        }

        return () => observer.disconnect();
    }, []);

    const handleLoad = () => {
        setIsLoaded(true);
    };

    const handleError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
        setHasError(true);
        if (onError) {
            onError(e);
        } else {
            const target = e.target as HTMLImageElement;
            target.src = placeholder;
        }
    };

    return (
        <div className={`relative ${className}`}>
            <img
                ref={imgRef}
                src={isInView ? src : placeholder}
                alt={alt}
                className={`transition-opacity duration-300 ${isLoaded ? "opacity-100" : "opacity-50"
                    } ${className}`}
                onLoad={handleLoad}
                onError={handleError}
                loading="lazy"
            />
            {!isLoaded && isInView && !hasError && (
                <div className="absolute inset-0 bg-gray-200 animate-pulse rounded" />
            )}
        </div>
    );
};

export default LazyImage;