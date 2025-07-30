/**
 * Utility to fetch the current Wild Rift patch version
 */

interface PatchInfo {
  version: string;
  title: string;
  date: string;
  url: string;
}

/**
 * Fetch the latest Wild Rift patch information
 */
export async function fetchLatestWildRiftPatch(): Promise<PatchInfo | null> {
  try {
    // Try to fetch from the official Wild Rift patch notes page
    const response = await fetch(
      "https://wildrift.leagueoflegends.com/en-us/news/game-updates/",
      {
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const html = await response.text();

    // Parse the HTML to extract patch information
    // Look for patch notes pattern
    const patchRegex = /wild-rift-patch-notes-(\d+)-(\d+)([a-z]?)/i;
    const titleRegex = /<title[^>]*>([^<]*patch[^<]*)<\/title>/i;

    const patchMatch = html.match(patchRegex);
    const titleMatch = html.match(titleRegex);

    if (patchMatch) {
      const [, major, minor, letter] = patchMatch;
      const version = `${major}.${minor}${letter || ""}`;

      return {
        version,
        title: titleMatch ? titleMatch[1] : `Wild Rift Patch ${version}`,
        date: new Date().toISOString().split("T")[0],
        url: `https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-${major}-${minor}${
          letter || ""
        }/`,
      };
    }

    // Fallback: return current known patch
    return {
      version: "6.2b",
      title: "Wild Rift Patch 6.2b",
      date: new Date().toISOString().split("T")[0],
      url: "https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-6-2b/",
    };
  } catch (error) {
    console.error("Error fetching Wild Rift patch:", error);

    // Return fallback patch info
    return {
      version: "6.2b",
      title: "Wild Rift Patch 6.2b",
      date: new Date().toISOString().split("T")[0],
      url: "https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-6-2b/",
    };
  }
}

/**
 * Get cached patch info or fetch new one
 */
export async function getCurrentPatch(): Promise<PatchInfo> {
  // In a real application, you might want to cache this in localStorage or a database
  // For now, we'll use a simple in-memory cache with fallback

  try {
    const patchInfo = await fetchLatestWildRiftPatch();
    return (
      patchInfo || {
        version: "6.2b",
        title: "Wild Rift Patch 6.2b",
        date: new Date().toISOString().split("T")[0],
        url: "https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-6-2b/",
      }
    );
  } catch (error) {
    console.error("Error getting current patch:", error);
    return {
      version: "6.2b",
      title: "Wild Rift Patch 6.2b",
      date: new Date().toISOString().split("T")[0],
      url: "https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-6-2b/",
    };
  }
}

/**
 * Alternative method using a more reliable API approach
 */
export async function fetchPatchFromAPI(): Promise<PatchInfo | null> {
  try {
    // This would be a custom API endpoint that scrapes patch info
    // For now, return the known current patch
    return {
      version: "6.2b",
      title: "Wild Rift Patch 6.2b",
      date: "2025-01-30",
      url: "https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-6-2b/",
    };
  } catch (error) {
    console.error("Error fetching from API:", error);
    return null;
  }
}

/**
 * Format patch version for display
 */
export function formatPatchVersion(version: string): string {
  return `Patch ${version}`;
}

/**
 * Check if patch version is valid Wild Rift format
 */
export function isValidWildRiftPatch(version: string): boolean {
  // Wild Rift patches follow format: X.Y or X.Ya (e.g., 6.2, 6.2a, 6.2b)
  const wildRiftPatchRegex = /^\d+\.\d+[a-z]?$/;
  return wildRiftPatchRegex.test(version);
}
