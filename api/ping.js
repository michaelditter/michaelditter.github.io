// Simple ping endpoint to test API connectivity
export default function handler(req, res) {
  // Set CORS headers
  const allowedOrigins = [
    'https://michaelditter.github.io', 
    'https://michaelditter.com', 
    'https://www.michaelditter.com'
  ];
  
  const origin = req.headers.origin;
  
  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  } else {
    res.setHeader('Access-Control-Allow-Origin', '*');
  }
  
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // Handle OPTIONS request
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  // Return a simple JSON response
  return res.status(200).json({ 
    success: true, 
    message: 'API is working!',
    timestamp: new Date().toISOString(),
    origin: origin || 'No origin header'
  });
} 