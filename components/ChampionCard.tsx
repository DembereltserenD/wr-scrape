import React, { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { useLanguage } from "../contexts/LanguageContext";
import { ChampionCard as ChampionCardType } from "../types/champion";
import LoadingSpinner from "./UI/LoadingSpinner";

interface ChampionCardProps {
  champion: ChampionCardType;
  showDetails?: boolean;
}

const ChampionCard: React.FC<ChampionCardProps> = ({
  champion,
  showDetails = true,
}) => {
  const { t } = useLanguage();
  const [imageLoading, setImageLoading] = useState(true);
  const [imageError, setImageError] = useState(false);

  const getTierColor = (tier: string): string => {
    const tierColors: Record<string, string> = {
      "S+": "bg-gradient-to-r from-red-500 to-red-600 text-white",
      S: "bg-gradient-to-r from-red-400 to-red-500 text-white",
      A: "bg-gradient-to-r from-orange-400 to-orange-500 text-white",
      B: "bg-gradient-to-r from-yellow-400 to-yellow-500 text-black",
      C: "bg-gradient-to-r from-green-400 to-green-500 text-white",
      D: "bg-gradient-to-r from-blue-400 to-blue-500 text-white",
    };
    return (
      tierColors[tier] ||
      "bg-gradient-to-r from-yellow-400 to-yellow-500 text-black"
    );
  };

  const getRoleTranslation = (role: string) => {
    // Clean up role string and map to translation keys
    const cleanRole = role.replace(/<\/?b>/g, "").trim();
    const roleMap: Record<string, string> = {
      Fighter: "roles.fighter",
      Tank: "roles.tank",
      "Fighter / Tank": "roles.fighter_tank",
      Assassin: "roles.assassin",
      Mage: "roles.mage",
      Marksman: "roles.marksman",
      Support: "roles.support",
    };

    const translationKey = roleMap[cleanRole];
    return translationKey ? t(translationKey) : cleanRole;
  };

  const getDifficultyColor = (difficulty: string): string => {
    const difficultyColors: Record<string, string> = {
      Low: "text-green-400",
      Medium: "text-yellow-400",
      High: "text-red-400",
      Easy: "text-green-400",
      Hard: "text-red-400",
    };
    return difficultyColors[difficulty] || "text-yellow-400";
  };

  const getStarRating = (tier: string): number => {
    const tierRatings: Record<string, number> = {
      "S+": 5,
      S: 5,
      A: 4,
      B: 3,
      C: 2,
      D: 1,
    };
    return tierRatings[tier] || 3;
  };

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, index) => (
      <svg
        key={index}
        className={`w-4 h-4 ${
          index < rating ? "text-yellow-400" : "text-gray-300"
        }`}
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
      </svg>
    ));
  };

  return (
    <Link href={`/champion/${champion.id}`} className="block">
      <div className="champion-card gaming-glow group transition-all duration-300 hover:scale-105 cursor-pointer">
        <div className="relative">
          {imageLoading && !imageError && (
            <div className="absolute inset-0 flex items-center justify-center bg-card-background">
              <LoadingSpinner size="md" color="primary" />
            </div>
          )}
          <Image
            src={
              imageError
                ? "/placeholder-champion.png"
                : champion.image || "/placeholder-champion.png"
            }
            alt={`${champion.name} - ${getRoleTranslation(champion.role)} champion`}
            width={300}
            height={192}
            className={`w-full h-48 object-cover transition-opacity duration-300 ${imageLoading ? "opacity-0" : "opacity-100"}`}
            placeholder="blur"
            blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAIAAoDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAhEAACAQMDBQAAAAAAAAAAAAABAgMABAUGIWGRkqGx0f/EABUBAQEAAAAAAAAAAAAAAAAAAAMF/8QAGhEAAgIDAAAAAAAAAAAAAAAAAAECEgMRkf/aAAwDAQACEQMRAD8AltJagyeH0AthI5xdrLcNM91BF5pX2HaH9bcfaSXWGaRmknyJckliyjqTzSlT54b6bk+h0R//2Q=="
            priority={false}
            loading="lazy"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            quality={85}
            onLoad={() => setImageLoading(false)}
            onError={() => {
              setImageError(true);
              setImageLoading(false);
            }}
          />

          {/* Tier Badge */}
          <div className="absolute top-2 right-2">
            <span
              className={`px-3 py-1 rounded-full text-sm font-bold shadow-lg ${getTierColor(champion.tier)}`}
            >
              {champion.tier} {t("champion.tier")}
            </span>
          </div>

          {/* Difficulty Badge */}
          <div className="absolute top-2 left-2">
            <span
              className={`bg-black bg-opacity-60 text-white px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(champion.difficulty)}`}
            >
              {t(`difficulty.${champion.difficulty.toLowerCase()}`)}
            </span>
          </div>
        </div>

        <div className="p-4">
          {/* Champion Name */}
          <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-1 group-hover:text-purple-600 transition-colors">
            {champion.name}
          </h3>

          {/* Role */}
          <div className="mb-3">
            <span className="bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 px-2 py-1 rounded text-sm font-medium">
              {getRoleTranslation(champion.role)}
            </span>
          </div>

          {/* Star Rating */}
          <div className="flex items-center mb-3">
            <div className="flex mr-2">
              {renderStars(getStarRating(champion.tier))}
            </div>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              ({getStarRating(champion.tier)}/5)
            </span>
          </div>

          {/* Lanes */}
          <div className="mb-3">
            <div className="flex flex-wrap gap-1">
              {champion.lanes.map((lane, index) => {
                // Map lane names to display names
                const displayLane =
                  lane === "Baron"
                    ? "Baron Lane"
                    : lane === "Mid"
                      ? "Mid Lane"
                      : lane === "Dragon"
                        ? "Dragon Lane"
                        : lane;

                return (
                  <span
                    key={index}
                    className="bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-2 py-1 rounded text-xs"
                  >
                    {displayLane}
                  </span>
                );
              })}
            </div>
          </div>

          {/* Win Rate and Pick Rate */}
          {(champion.winRate || champion.pickRate) && (
            <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-3">
              {champion.winRate && (
                <span>
                  {t("champion.win_rate")}: {champion.winRate}
                </span>
              )}
              {champion.pickRate && (
                <span>
                  {t("champion.pick_rate")}: {champion.pickRate}
                </span>
              )}
            </div>
          )}

          {/* Details Link */}
          {showDetails && (
            <Link
              href={`/champion/${champion.id}`}
              className="inline-flex items-center text-purple-600 hover:text-purple-800 dark:text-purple-400 dark:hover:text-purple-300 text-sm font-medium group-hover:underline transition-colors"
            >
              {t("sections.details")}
              <svg
                className="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </Link>
          )}
        </div>
      </div>
    </Link>
  );
};

export default ChampionCard;
