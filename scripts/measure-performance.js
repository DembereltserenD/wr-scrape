const {
    performance
} = require('perf_hooks');
const fs = require('fs');
const path = require('path');

/**
 * Measure champion page build performance
 */
async function measurePerformance() {
    console.log('🔍 Measuring champion page performance...');

    const startTime = performance.now();

    try {
        // Test the cache system directly with the index
        const indexPath = path.join(process.cwd(), 'champion_index.json');
        const championsPath = path.join(process.cwd(), 'champions_clean');

        if (!fs.existsSync(indexPath)) {
            console.log('❌ Champion index not found. Run: node scripts/build-champion-index.js');
            process.exit(1);
        }

        console.log('📊 Testing cache performance...');

        // Measure index loading
        const indexStart = performance.now();
        const indexData = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
        const slugs = Object.keys(indexData);
        const indexTime = performance.now() - indexStart;

        console.log(`✅ Index loaded in ${indexTime.toFixed(2)}ms for ${slugs.length} champions`);

        // Measure champion loading
        const loadStart = performance.now();
        const testChampions = slugs.slice(0, 10); // Test first 10 champions

        for (const slug of testChampions) {
            const championStart = performance.now();

            // Simulate champion loading
            const entry = indexData[slug];
            if (entry) {
                const filePath = path.join(championsPath, entry.filename);
                const content = fs.readFileSync(filePath, 'utf-8');
                const rawData = JSON.parse(content);

                const championTime = performance.now() - championStart;
                console.log(`⚡ ${rawData.name || slug}: ${championTime.toFixed(2)}ms`);
            }
        }

        const totalLoadTime = performance.now() - loadStart;
        const avgLoadTime = totalLoadTime / testChampions.length;

        console.log(`\n📈 Performance Results:`);
        console.log(`- Index load time: ${indexTime.toFixed(2)}ms`);
        console.log(`- Average champion load time: ${avgLoadTime.toFixed(2)}ms`);
        console.log(`- Total test time: ${(performance.now() - startTime).toFixed(2)}ms`);

        // Performance targets
        const targets = {
            indexLoad: 50, // ms
            championLoad: 20, // ms
        };

        console.log(`\n🎯 Performance Targets:`);
        console.log(`- Index load: ${indexTime <= targets.indexLoad ? '✅' : '❌'} ${indexTime.toFixed(2)}ms (target: ${targets.indexLoad}ms)`);
        console.log(`- Champion load: ${avgLoadTime <= targets.championLoad ? '✅' : '❌'} ${avgLoadTime.toFixed(2)}ms (target: ${targets.championLoad}ms)`);

        // Estimate build time improvement
        const oldEstimate = slugs.length * 150; // Old system ~150ms per champion
        const newEstimate = indexTime + (slugs.length * avgLoadTime);
        const improvement = ((oldEstimate - newEstimate) / oldEstimate * 100);

        console.log(`\n🚀 Estimated Build Time Improvement:`);
        console.log(`- Old system: ~${(oldEstimate / 1000).toFixed(1)}s`);
        console.log(`- New system: ~${(newEstimate / 1000).toFixed(1)}s`);
        console.log(`- Improvement: ${improvement.toFixed(1)}% faster`);

        // Memory usage
        const memUsage = process.memoryUsage();
        console.log(`\n💾 Memory Usage:`);
        console.log(`- RSS: ${(memUsage.rss / 1024 / 1024).toFixed(2)} MB`);
        console.log(`- Heap Used: ${(memUsage.heapUsed / 1024 / 1024).toFixed(2)} MB`);

    } catch (error) {
        console.error('❌ Performance test failed:', error);
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    measurePerformance();
}

module.exports = {
    measurePerformance
};