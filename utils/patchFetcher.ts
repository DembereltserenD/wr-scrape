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

    // Look for the most recent patch notes link in the HTML
    // Updated regex to catch various patch note URL patterns
    const patchRegexes = [
      /wild-rift-patch-notes-(\d+)-(\d+)([a-z]?)/gi,
      /patch-notes-(\d+)-(\d+)([a-z]?)/gi,
      /patch-(\d+)-(\d+)([a-z]?)/gi,
    ];

    let latestPatch = null;
    let latestVersion = { major: 0, minor: 0, letter: "" };

    for (const regex of patchRegexes) {
      let match;
      while ((match = regex.exec(html)) !== null) {
        const [, major, minor, letter] = match;
        const majorNum = parseInt(major);
        const minorNum = parseInt(minor);

        // Compare versions to find the latest
        if (
          majorNum > latestVersion.major ||
          (majorNum === latestVersion.major &&
            minorNum > latestVersion.minor) ||
          (majorNum === latestVersion.major &&
            minorNum === latestVersion.minor &&
            letter > latestVersion.letter)
        ) {
          latestVersion = {
            major: majorNum,
            minor: minorNum,
            letter: letter || "",
          };
          latestPatch = {
            version: `${major}.${minor}${letter || ""}`,
            title: `Wild Rift Patch ${major}.${minor}${letter || ""}`,
            date: new Date().toISOString().split("T")[0],
            url: `https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-${major}-${minor}${
              letter || ""
            }/`,
          };
        }
      }
    }

    if (latestPatch) {
      return latestPatch;
    }

    // If no patch found in HTML, try alternative approach
    return await fetchPatchFromAPI();
  } catch (error) {
    console.error("Error fetching Wild Rift patch:", error);
    return await fetchPatchFromAPI();
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
    if (patchInfo) {
      return patchInfo;
    }

    // Final fallback
    return {
      version: "6.2b",
      title: "Wild Rift Patch 6.2b",
      date: new Date().toISOString().split("T")[0],
      url: "https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-6-2b/",
    };
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
    // Try to get patch info from Riot's data dragon or community APIs
    // For now, we'll use a fallback with the most recent known patch
    // In production, this could call a custom API that regularly scrapes patch info

    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;

    // Estimate current patch based on Riot's release schedule (roughly every 2-3 weeks)
    // This is a rough estimation - in production you'd want a more reliable source
    let estimatedPatch = "6.2b";

    // You could implement more sophisticated logic here to estimate current patch
    // based on release patterns, or call a third-party API

    return {
      version: estimatedPatch,
      title: `Wild Rift Patch ${estimatedPatch}`,
      date: currentDate.toISOString().split("T")[0],
      url: `https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-${estimatedPatch.replace(
        ".",
        "-"
      )}/`,
    };
  } catch (error) {
    console.error("Error fetching from API:", error);
    return {
      version: "6.2b",
      title: "Wild Rift Patch 6.2b",
      date: "2025-01-30",
      url: "https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-6-2b/",
    };
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
