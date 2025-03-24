// Replit Setup Script
// This script will run automatically in Replit to initialize the environment

const fs = require('fs');
const { execSync } = require('child_process');

console.log('🚀 Setting up Michael Ditter Website in Replit...');

// Check if package.json exists
if (!fs.existsSync('./package.json')) {
  console.error('❌ package.json not found. Cannot proceed with setup.');
  process.exit(1);
}

// Install dependencies
try {
  console.log('📦 Installing dependencies...');
  execSync('npm install', { stdio: 'inherit' });
  console.log('✅ Dependencies installed successfully.');
} catch (error) {
  console.error('❌ Failed to install dependencies:', error.message);
  process.exit(1);
}

// Create necessary directories if they don't exist
const directories = ['./bitcoin-research-api/api', './ai-research-api/api'];
directories.forEach(dir => {
  if (!fs.existsSync(dir)) {
    try {
      console.log(`📁 Creating directory: ${dir}`);
      fs.mkdirSync(dir, { recursive: true });
      console.log(`✅ Created directory: ${dir}`);
    } catch (error) {
      console.error(`❌ Failed to create directory ${dir}:`, error.message);
    }
  }
});

// Check if the bitcoin-data.js API file exists, if not create a sample
const bitcoinApiFile = './bitcoin-research-api/api/bitcoin-data.js';
if (!fs.existsSync(bitcoinApiFile)) {
  try {
    console.log('📝 Creating sample Bitcoin API file...');
    const sampleBitcoinApi = `// Sample Bitcoin API data
module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    // Generate sample data
    const currentPrice = 84570 + Math.floor(Math.random() * 2000 - 1000);
    const weeklyChange = (Math.random() * 10 - 5).toFixed(2);
    
    const data = {
      reportDate: new Date().toISOString().split('T')[0],
      bitcoinPrice: {
        current: \`\$\${currentPrice.toLocaleString()}\`,
        weeklyChange: \`\${weeklyChange}%\`,
        weeklyTrend: weeklyChange > 0 ? "up" : "down"
      },
      marketSummary: {
        marketCap: \`\$\${(currentPrice * 19500000 / 1000000000000).toFixed(2)} trillion\`,
        volume24h: \`\$\${(Math.random() * 50 + 20).toFixed(2)} billion\`,
        dominance: \`\${(Math.random() * 5 + 55).toFixed(2)}%\`
      },
      keyInsights: [
        {
          title: "Institutional Adoption Accelerates",
          content: "Major financial institutions including Fidelity and BlackRock continue to increase their Bitcoin holdings, with an estimated $2.3 billion in new institutional investments this week.",
          source: "Bloomberg Financial",
          date: new Date().toISOString().split('T')[0]
        },
        {
          title: "SEC Bitcoin ETF Decision Pending",
          content: "The SEC is expected to announce decisions on several Bitcoin ETF applications in the coming weeks, potentially opening the door to greater mainstream investment.",
          source: "Wall Street Journal",
          date: new Date().toISOString().split('T')[0]
        },
        {
          title: "Lightning Network Capacity Hits New High",
          content: "Bitcoin's Layer 2 scaling solution, the Lightning Network, has reached a new all-time high of 5,000+ BTC capacity, improving Bitcoin's viability for everyday transactions.",
          source: "Bitcoin Magazine",
          date: new Date().toISOString().split('T')[0]
        }
      ]
    };
    
    // Return the data
    return res.status(200).json(data);
  } catch (error) {
    console.error('Error generating Bitcoin data:', error);
    return res.status(500).json({ 
      error: 'Internal Server Error',
      message: process.env.NODE_ENV === 'development' ? error.message : 'An unexpected error occurred'
    });
  }
};`;
    fs.writeFileSync(bitcoinApiFile, sampleBitcoinApi);
    console.log('✅ Created sample Bitcoin API file.');
  } catch (error) {
    console.error('❌ Failed to create sample Bitcoin API file:', error.message);
  }
}

// Create a simple vercel.json config if it doesn't exist
const vercelConfig = './bitcoin-research-api/vercel.json';
if (!fs.existsSync(vercelConfig)) {
  try {
    console.log('📝 Creating Vercel config file...');
    const sampleVercelConfig = `{
  "version": 2,
  "builds": [
    { "src": "api/**/*.js", "use": "@vercel/node" }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/$1" }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}`;
    fs.writeFileSync(vercelConfig, sampleVercelConfig);
    console.log('✅ Created Vercel config file.');
  } catch (error) {
    console.error('❌ Failed to create Vercel config file:', error.message);
  }
}

console.log('🎉 Setup complete! You can now run the website with "npm run dev"');
console.log('🌐 The Bitcoin report and AI charts should work out of the box in Replit');
console.log('📊 Visit the website preview to see your changes');
console.log('\n⚠️ Note: If you encounter any issues, check the browser console for errors.'); 