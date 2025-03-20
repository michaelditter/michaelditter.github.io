// Serverless API function to provide AI research data
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

// API data sources
const SOURCES = {
  ARXIV: 'https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=10',
  NEWS_API: 'https://newsapi.org/v2/everything?q=artificial+intelligence&language=en&sortBy=publishedAt',
  TECH_CRUNCH: 'https://techcrunch.com/wp-json/wp/v2/posts?categories=424613,17396,576603445&per_page=5',
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
    
    // For now, serve the sample data directly
    // In a production environment, you would fetch real-time data
    // from various sources (arXiv, tech blogs, news APIs, etc.)
    
    // Sample data structure - in a real implementation, this would be fetched
    // from external APIs and transformed
    const data = {
      "AI Model Updates": [
        {
          "title": "Claude 3.5 Sonnet Released: Outperforms GPT-4o in Reasoning Tasks",
          "summary": "Anthropic has released Claude 3.5 Sonnet, a new version of their AI assistant that surpasses GPT-4o in reasoning capabilities. The model demonstrates improved performance on complex tasks involving multi-step problem solving and instruction following.",
          "description_md": "### Claude 3.5 Sonnet Makes Significant Strides\n\nAnthropic's latest model shows a 31% improvement on reasoning benchmarks compared to Claude 3 Opus. Key improvements include:\n\n- Advanced mathematical reasoning capabilities\n- Enhanced code generation and debugging\n- Better context retention across long conversations\n- More nuanced understanding of ambiguous instructions\n\nBenchmark results indicated a 15% performance gain over GPT-4o on reasoning tasks, although GPT-4o still maintains advantages in certain creative tasks.",
          "link": "https://www.anthropic.com/research/claude-3-5-sonnet",
          "date": new Date().toISOString().split('T')[0],
          "image_url": "https://www.michaelditter.com/img/ai-research/claude-3-5-sonnet.jpg",
          "tags": ["LLMs", "Anthropic", "Claude", "Reasoning"]
        },
        {
          "title": "Meta's Llama 4 Brings Multimodal Capabilities to Open Source Models",
          "summary": "Meta has announced Llama 4, its latest family of large language models that includes robust multimodal capabilities. The new models can process and reason about images, text, and soon audio inputs within a single system.",
          "link": "https://ai.meta.com/blog/llama-4/",
          "date": new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          "image_url": "https://www.michaelditter.com/img/ai-research/llama-4.jpg",
          "tags": ["LLMs", "Meta", "Llama", "Multimodal", "Open Source"]
        },
        {
          "title": "DeepMind's AlphaCode 2 Achieves Competitive Programming Breakthrough",
          "summary": "Google DeepMind has unveiled AlphaCode 2, which can now solve advanced competitive programming problems at the level of gold medalists in international competitions. The system combines sophisticated code generation with automatic verification methods.",
          "link": "https://deepmind.google/research/alphacode-2/",
          "date": new Date(Date.now() - 9 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          "tags": ["DeepMind", "Code Generation", "AI Programming"]
        }
      ],
      "Hardware Advancements": [
        {
          "title": "NVIDIA Unveils H300 Tensor Chip: 5x Performance Leap for AI Training",
          "summary": "NVIDIA has announced the H300 Tensor Core GPU, delivering a 5x performance improvement for AI training workloads compared to the previous H200 series. The chip incorporates new architecture optimizations specifically designed for large language model training.",
          "description_md": "## H300: The Next Generation of AI Accelerators\n\nNVIDIA's H300 represents a significant leap forward in compute capability:\n\n- New Tensor Core architecture with 4th-gen FP8 precision\n- 1.1 TB/s memory bandwidth with HBM4 memory\n- 1,600 TFLOPS FP8 peak performance\n- 70% power efficiency improvement per FLOP\n- Support for model parallelism across 32,000+ GPUs\n\nThe H300 is expected to enter production in Q4 2025 and will significantly reduce the time and cost required to train foundation models with trillions of parameters.",
          "link": "https://nvidia.com/h300-announcement",
          "date": new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          "image_url": "https://www.michaelditter.com/img/ai-research/nvidia-h300.jpg",
          "tags": ["NVIDIA", "GPU", "AI Hardware", "HBM4"]
        }
      ],
      "Robotics": [
        {
          "title": "Boston Dynamics' Atlas Humanoid Robot Enters Commercial Production",
          "summary": "Boston Dynamics has announced that its Atlas humanoid robot is entering commercial production, marking a significant milestone for versatile bipedal robots. The commercial version can lift 35kg and navigate complex environments autonomously.",
          "link": "https://bostondynamics.com/atlas-commercial",
          "date": new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          "tags": ["Boston Dynamics", "Humanoid Robots", "Robotics"]
        }
      ],
      "Enterprise AI": [
        {
          "title": "McKinsey Study: AI Implementation Increases Productivity by 37% in Financial Services",
          "summary": "A new McKinsey study shows financial services companies implementing enterprise AI solutions have seen productivity increases averaging 37%. The largest gains came from automating document processing and enhancing customer service operations.",
          "link": "https://mckinsey.com/finance-ai-productivity-2025",
          "date": new Date().toISOString().split('T')[0],
          "tags": ["Financial Services", "Productivity", "McKinsey", "ROI"]
        }
      ],
      "Regulatory News": [
        {
          "title": "EU AI Act Enforcement Guidelines Released, Implementation Timeline Clarified",
          "summary": "The European Commission has released enforcement guidelines for the EU AI Act, providing clarity on implementation timelines. Critical AI systems must comply by January 2026, while general-purpose AI systems have until July 2026.",
          "link": "https://digital-strategy.ec.europa.eu/ai-act-enforcement",
          "date": new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          "tags": ["EU AI Act", "Regulation", "Compliance", "Europe"]
        }
      ],
      "Research": [
        {
          "title": "MIT Researchers Develop Framework for Measuring AI Alignment",
          "summary": "MIT researchers have introduced a quantitative framework for measuring AI alignment with human values. The approach uses a combination of benchmarks, red-teaming exercises, and statistical methods to evaluate how well AI systems adhere to human intent.",
          "link": "https://mit.edu/csail/ai-alignment-measurement",
          "date": new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          "tags": ["MIT", "AI Alignment", "Safety", "Measurement"]
        }
      ],
      "Future Trends": [
        {
          "title": "Gartner Predicts 65% of Enterprises Will Use Multimodal AI by 2027",
          "summary": "Gartner's latest forecast predicts that 65% of enterprises will deploy multimodal AI applications by 2027, up from just 15% in 2025. The adoption will be driven by improved user interfaces, document processing, and multimedia content analysis.",
          "link": "https://gartner.com/ai-predictions-2027",
          "date": new Date().toISOString().split('T')[0],
          "tags": ["Gartner", "Multimodal AI", "Enterprise", "Predictions"]
        }
      ]
    };
    
    // Update cache
    cachedData = data;
    cacheTime = now;
    
    // Return the data
    return res.status(200).json(data);
  } catch (error) {
    console.error('Error generating AI research data:', error);
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