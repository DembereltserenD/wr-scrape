import React, { useState, useEffect } from 'react';
import { getCurrentPatch, formatPatchVersion } from '../utils/patchFetcher';

interface PatchInfoProps {
    className?: string;
    showLink?: boolean;
}

const PatchInfo: React.FC<PatchInfoProps> = ({
    className = "bg-primary-purple text-white px-3 py-1 rounded-full text-sm font-medium",
    showLink = false
}) => {
    const [patchInfo, setPatchInfo] = useState({
        version: '6.2b',
        url: 'https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-6-2b/'
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

    if (loading) {
        return (
            <span className={className}>
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
                className={`${className} hover:opacity-80 transition-opacity cursor-pointer`}
                title="View patch notes"
            >
                {content}
            </a>
        );
    }

    return (
        <span className={className}>
            {content}
        </span>
    );
};

export default PatchInfo;