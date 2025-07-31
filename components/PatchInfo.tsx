import React, { useState, useEffect } from 'react';
import { getCurrentPatch, formatPatchVersion } from '../utils/patchFetcher';

interface PatchInfoProps {
    className?: string;
    showLink?: boolean;
}

const PatchInfo: React.FC<PatchInfoProps> = ({
    className,
    showLink = false
}) => {
    const [patchInfo, setPatchInfo] = useState({
        version: 'Loading...',
        url: '#'
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPatch = async () => {
            try {
                const info = await getCurrentPatch();
                setPatchInfo({
                    version: info.version,
                    url: info.url
                });
            } catch (error) {
                console.error('Error fetching patch info:', error);
                // Keep default values
            } finally {
                setLoading(false);
            }
        };

        fetchPatch();
    }, []);

    // Default button styling
    const defaultButtonClass = "inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary-purple to-accent-pink text-white font-semibold rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200 border border-primary-purple/30";
    const defaultSpanClass = "bg-primary-purple text-white px-3 py-1 rounded-full text-sm font-medium";

    if (loading) {
        return (
            <span className={className || defaultSpanClass}>
                Loading...
            </span>
        );
    }

    const content = formatPatchVersion(patchInfo.version);

    if (showLink) {
        return (
            <a
                href={patchInfo.url}
                target="_blank"
                rel="noopener noreferrer"
                className={className || defaultButtonClass}
                title="View patch notes"
            >
                <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                </svg>
                {content}
                <svg
                    className="w-3 h-3 opacity-70"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                    />
                </svg>
            </a>
        );
    }

    return (
        <span className={className || defaultSpanClass}>
            {content}
        </span>
    );
};

export default PatchInfo;