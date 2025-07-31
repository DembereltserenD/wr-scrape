const fs = require('fs');
const path = require('path');

/**
 * Pre-build champion index for faster builds
 */
function buildChampionIndex() {
    console.log('🚀 Building champion index...');

    const championsPath = path.join(process.cwd(), 'champions_clean');
    const indexPath = path.join(process.cwd(), 'champion_index.json');

    if (!fs.existsSync(championsPath)) {
        console.error('❌ Champions directory not found');
        process.exit(1);
    }

    const index = {};
    const files = fs.readdirSync(championsPath);
    let processed = 0;

    for (const file of files) {
        if (!file.endsWith('.json')) continue;

        try {
            const filePath = path.join(championsPath, file);
            const content = fs.readFileSync(filePath, 'utf-8');

            // Parse only the minimal data needed for index
            const data = JSON.parse(content);
            const slug = file.replace('.json', '');

            index[slug] = {
                filename: file,
                name: data.name || slug,
                tier: data.tier?.toString() || '3',
                role: data.roles?. [0] || 'Unknown'
            };

            processed++;
        } catch (error) {
            console.warn(`⚠️  Failed to index champion ${file}:`, error.message);
        }
    }

    // Write index file
    fs.writeFileSync(indexPath, JSON.stringify(index, null, 2));

    console.log(`✅ Champion index built successfully!`);
    console.log(`📊 Processed ${processed} champions`);
    console.log(`💾 Index saved to: ${indexPath}`);
}

// Run if called directly
if (require.main === module) {
    buildChampionIndex();
}

module.exports = {
    buildChampionIndex
};