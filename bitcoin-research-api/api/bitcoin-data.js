// Serverless API function to provide Bitcoin research data
// Deploy to Vercel or similar serverless platform

// Import needed packages (for local testing, run: npm install axios node-cache)
// Uncomment for local development:
// const axios = require('axios');
// const NodeCache = require('node-cache');

// In-memory cache with 1 hour TTL
let cachedData = null;
let cacheTime = 0;
const CACHE_TTL = 3600 * 1000; // 1 hour in milliseconds

// Rate limiting
const RATE_LIMIT_WINDOW = 60 * 1000; // 1 minute window
const MAX_REQUESTS_PER_WINDOW = 10;
const ipRequests = new Map();

// API data sources for Bitcoin data
const SOURCES = {
  COINDESK_API: 'https://api.coindesk.com/v1/bpi/currentprice.json',
  COINGECKO_API: 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7&interval=daily',
  CRYPTO_NEWS_API: 'https://cryptonews-api.com/api/v1/category?section=general&items=10',
  // Add more sources as needed
};

/**
 * Basic rate limiting middleware
 */
function checkRateLimit(req) {
  const now = Date.now();
  const ip = req.headers['x-forwarded-for'] || 'unknown';
  
  // Clean up old entries
  for (const [ipAddr, requestInfo] of ipRequests.entries()) {
    if (now - requestInfo.windowStart > RATE_LIMIT_WINDOW) {
      ipRequests.delete(ipAddr);
    }
  }
  
  // Check current IP
  if (!ipRequests.has(ip)) {
    ipRequests.set(ip, { count: 1, windowStart: now });
    return true;
  }
  
  const requestInfo = ipRequests.get(ip);
  
  // Reset window if needed
  if (now - requestInfo.windowStart > RATE_LIMIT_WINDOW) {
    requestInfo.count = 1;
    requestInfo.windowStart = now;
    return true;
  }
  
  // Increment and check
  requestInfo.count += 1;
  return requestInfo.count <= MAX_REQUESTS_PER_WINDOW;
}

/**
 * Main handler for the API request
 */
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
  
  // Check API key for authorization (disabled by default)
  const requireApiKey = process.env.REQUIRE_API_KEY === 'true';
  const authHeader = req.headers.authorization;
  if (requireApiKey && (!authHeader || !validateApiKey(authHeader))) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  // Check rate limit
  if (!checkRateLimit(req)) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  
  try {
    // If we have cached data that's not expired, return it
    const now = Date.now();
    if (cachedData && (now - cacheTime < CACHE_TTL)) {
      console.log('Serving from cache');
      return res.status(200).json(cachedData);
    }
    
    // Get current date for the report
    const today = new Date();
    const reportDate = today.toISOString().split('T')[0];
    
    // Focus only on data from the last 7 days
    const oneWeekAgo = new Date(today);
    oneWeekAgo.setDate(today.getDate() - 7);
    
    // For now, serve the sample data directly
    // In a production environment, you would fetch real-time data
    // from various Bitcoin and cryptocurrency APIs
    
    // Generate random price movement for demo
    const currentPrice = 84570 + Math.floor(Math.random() * 2000 - 1000); // Random fluctuation around $84,570
    const weeklyChange = (Math.random() * 10 - 5).toFixed(2); // Random between -5% and +5%
    
    // Sample data structure - in a real implementation, this would be fetched
    // from crypto APIs and transformed
    const data = {
      reportDate: reportDate,
      bitcoinPrice: {
        current: `$${currentPrice.toLocaleString()}`,
        weeklyChange: `${weeklyChange}%`,
        weeklyTrend: weeklyChange > 0 ? "up" : "down"
      },
      marketSummary: {
        marketCap: `$${(currentPrice * 19500000 / 1000000000000).toFixed(2)} trillion`,
        volume24h: `$${(Math.random() * 50 + 20).toFixed(2)} billion`,
        dominance: `${(Math.random() * 5 + 55).toFixed(2)}%`
      },
      keyInsights: [
        {
          title: "Institutional Adoption Accelerates",
          content: "Major financial institutions including Fidelity and BlackRock continue to increase their Bitcoin holdings, with an estimated $2.3 billion in new institutional investments this week.",
          source: "Bloomberg Financial",
          date: new Date(Date.now() - Math.floor(Math.random() * 7) * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        },
        {
          title: "SEC Bitcoin ETF Decision Pending",
          content: "The SEC is expected to announce decisions on several Bitcoin ETF applications in the coming weeks, potentially opening the door to greater mainstream investment.",
          source: "Wall Street Journal",
          date: new Date(Date.now() - Math.floor(Math.random() * 7) * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        },
        {
          title: "Lightning Network Capacity Hits New High",
          content: "Bitcoin's Layer 2 scaling solution, the Lightning Network, has reached a new all-time high of 5,000+ BTC capacity, improving Bitcoin's viability for everyday transactions.",
          source: "Bitcoin Magazine",
          date: new Date(Date.now() - Math.floor(Math.random() * 7) * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        }
      ],
      technicalAnalysis: {
        supportLevels: ["$79,500", "$77,800", "$75,200"],
        resistanceLevels: ["$86,500", "$90,000", "$100,000"],
        indicators: {
          rsi: (Math.random() * 30 + 40).toFixed(2), // Random between 40-70
          macd: "Bullish crossover forming",
          movingAverages: "Trading above all major MAs"
        }
      },
      regulatoryUpdates: [
        {
          region: "United States",
          development: "Treasury Department clarifies reporting requirements for cryptocurrency transactions above $10,000.",
          impact: "Moderate",
          date: new Date(Date.now() - Math.floor(Math.random() * 7) * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        },
        {
          region: "European Union",
          development: "EU MiCA regulations implementation timeline announced, with full compliance required by Q2 2025.",
          impact: "Significant",
          date: new Date(Date.now() - Math.floor(Math.random() * 7) * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        }
      ],
      upcomingEvents: [
        {
          name: "Bitcoin Amsterdam Conference",
          date: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          significance: "Major industry gathering with key announcements expected"
        },
        {
          name: "Bitcoin Core Developer Meeting",
          date: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          significance: "Discussion of upcoming protocol improvements"
        }
      ],
      outlook: {
        shortTerm: "Bullish, with potential volatility around ETF decisions",
        midTerm: "Strong upward momentum expected to continue through Q3",
        keyRisks: [
          "Regulatory uncertainty in key markets",
          "Macroeconomic headwinds affecting risk assets",
          "Technical resistance at psychological $100K level"
        ]
      }
    };
    
    // Update cache
    cachedData = data;
    cacheTime = now;
    
    // Return the data
    return res.status(200).json(data);
  } catch (error) {
    console.error('Error generating Bitcoin research data:', error);
    return res.status(500).json({ 
      error: 'Internal Server Error',
      message: process.env.NODE_ENV === 'development' ? error.message : 'An unexpected error occurred'
    });
  }
};

/**
 * Validate the API key from the Authorization header
 */
function validateApiKey(authHeader) {
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return false;
  }
  
  const apiKey = authHeader.substring(7); // Remove 'Bearer ' prefix
  // In production, you would validate against a database or environment variable
  return apiKey === process.env.API_KEY;
}

// For local testing only - uncomment and run with Node.js
/*
if (require.main === module) {
  // Mock express req/res for local testing
  const req = { 
    method: 'GET',
    headers: { 'x-forwarded-for': '127.0.0.1' }
  };
  const res = {
    setHeader: (name, value) => console.log(`Setting header ${name}: ${value}`),
    status: (code) => {
      console.log(`Status: ${code}`);
      return {
        json: (data) => console.log(JSON.stringify(data, null, 2)),
        end: () => console.log('Response ended')
      };
    }
  };
  
  // Call the handler
  module.exports(req, res);
}
*/ 