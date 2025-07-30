import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { ChampionStats } from "../types/champion";
import { useTranslation } from "../utils/i18n";

interface ChampionStatsPieChartProps {
  stats: ChampionStats;
}

const ChampionStatsPieChart: React.FC<ChampionStatsPieChartProps> = ({
  stats,
}) => {
  const { t } = useTranslation();

  // Individual stat configurations
  const statConfigs = [
    {
      name: "damage",
      value: stats.damage?.base || 0,
      color: "#ef4444", // red-500
      emoji: "⚔️",
      label: t("stats.damage") || "Damage",
    },
    {
      name: "toughness",
      value: stats.toughness?.base || 0,
      color: "#22c55e", // green-500
      emoji: "🛡️",
      label: t("stats.toughness") || "Toughness",
    },
    {
      name: "utility",
      value: stats.utility?.base || 0,
      color: "#3b82f6", // blue-500
      emoji: "🔧",
      label: t("stats.utility") || "Utility",
    },
    {
      name: "difficulty",
      value: stats.difficulty?.base || 0,
      color: "#a855f7", // purple-500
      emoji: "📚",
      label: t("stats.difficulty") || "Difficulty",
    },
  ];

  // Create individual pie chart for each stat
  const createStatPieChart = (statConfig: any) => {
    const data = [
      {
        name: "filled",
        value: statConfig.value,
        color: statConfig.color,
      },
      {
        name: "empty",
        value: 100 - statConfig.value,
        color: "#374151", // gray-700
      },
    ];

    const CustomTooltip = ({ active, payload }: any) => {
      if (active && payload && payload.length && payload[0].name === "filled") {
        return (
          <div className="bg-slate-800 border border-slate-600 rounded-lg p-3 shadow-lg">
            <p className="text-white font-semibold">
              {statConfig.emoji} {statConfig.label}
            </p>
            <p className="text-gray-300">
              Value:{" "}
              <span className="font-bold" style={{ color: statConfig.color }}>
                {statConfig.value}
              </span>
            </p>
          </div>
        );
      }
      return null;
    };

    return (
      <div key={statConfig.name} className="flex flex-col items-center">
        <div className="w-32 h-32 relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={35}
                outerRadius={60}
                startAngle={90}
                endAngle={450}
                dataKey="value"
                stroke="none"
              >
                {data.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.color}
                    className={
                      index === 0
                        ? "hover:opacity-80 transition-opacity duration-200 cursor-pointer"
                        : ""
                    }
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>

          {/* Center text */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className="text-2xl mb-1">{statConfig.emoji}</div>
            <div
              className="text-lg font-bold"
              style={{ color: statConfig.color }}
            >
              {statConfig.value}
            </div>
          </div>
        </div>

        {/* Label */}
        <div className="mt-2 text-center">
          <div className="text-sm font-medium text-gray-300">
            {statConfig.label}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
      <h3 className="text-xl font-bold mb-6 text-white text-center">
        {t("stats.title") || "Champion Stats"}
      </h3>

      {/* Individual Pie Charts Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 justify-items-center">
        {statConfigs.map(createStatPieChart)}
      </div>

      {/* Stats Summary Cards */}
      <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
        {statConfigs.map((stat) => (
          <div
            key={stat.name}
            className="bg-slate-700/50 p-3 rounded-md border border-slate-600/50 text-center hover:bg-slate-700/70 transition-colors duration-200"
          >
            <div className="text-2xl mb-1">{stat.emoji}</div>
            <div className="text-sm font-medium text-gray-300 mb-1">
              {stat.label}
            </div>
            <div className="text-lg font-bold" style={{ color: stat.color }}>
              {stat.value}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChampionStatsPieChart;
