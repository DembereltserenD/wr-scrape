const {
    ChampionDataLoader
} = require('./utils/dataLoader.ts');

// Test loading Zed specifically
console.log('Testing Zed champion data loading...');

try {
    // Load Zed's data
    const zedData = ChampionDataLoader.loadChampion('zed.json');

    if (zedData) {
        console.log('✅ Zed data loaded successfully!');
        console.log('Champion Name:', zedData.champion.name);
        console.log('Champion ID:', zedData.champion.id);
        console.log('Role:', zedData.champion.role);
        console.log('Tier:', zedData.champion.tier);
        console.log('Difficulty:', zedData.champion.difficulty);
        console.log('Lanes:', zedData.champion.lanes);
        console.log('Image URL:', zedData.champion.image);

        // Test filtering
        const allChampions = ChampionDataLoader.loadAllChampions();
        const zedFromAll = allChampions.find(c => c.champion.name === 'ZED');

        if (zedFromAll) {
            console.log('✅ Zed found in all champions list');
            console.log('Zed in all champions - Tier:', zedFromAll.champion.tier);
        } else {
            console.log('❌ Zed not found in all champions list');
        }

        // Test lane filtering
        const midChampions = allChampions.filter(c => c.champion.lanes.includes('Mid'));
        const zedInMid = midChampions.find(c => c.champion.name === 'ZED');

        if (zedInMid) {
            console.log('✅ Zed found in Mid lane champions');
        } else {
            console.log('❌ Zed not found in Mid lane champions');
        }

    } else {
        console.log('❌ Failed to load Zed data');
    }

} catch (error) {
    console.error('Error testing Zed data:', error);
}