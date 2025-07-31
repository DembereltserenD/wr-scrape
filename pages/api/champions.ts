import { NextApiRequest, NextApiResponse } from "next";
import { ChampionDataLoader } from "../../utils/dataLoader";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === "GET") {
    try {
      const champions = ChampionDataLoader.loadAllChampions();

      // Return simplified champion data for search
      const simplifiedChampions = champions.map((champion) => ({
        champion: {
          id: champion.champion.id,
          name: champion.champion.name,
          role: champion.champion.role,
          tier: champion.champion.tier,
          image: champion.champion.image,
          lanes: champion.champion.lanes,
        },
      }));

      res.status(200).json(simplifiedChampions);
    } catch (error) {
      console.error("Error loading champions for API:", error);
      res.status(500).json({ error: "Failed to load champions" });
    }
  } else {
    res.setHeader("Allow", ["GET"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
