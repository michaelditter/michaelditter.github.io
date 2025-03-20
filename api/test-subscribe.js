// Simple test API endpoint with explicit CORS headers
export default async function handler(req, res) {
  // Log the request details for debugging
  console.log(`[${new Date().toISOString()}] Test Subscribe API called`);
  console.log(`Method: ${req.method}`);
  console.log(`Origin: ${req.headers.origin || 'unknown'}`);
  console.log(`Headers: ${JSON.stringify(req.headers)}`);
  
  // Define allowed origins
  const allowedOrigins = [
    'https://michaelditter.github.io', 
    'https://michaelditter.com', 
    'https://www.michaelditter.com'
  ];
  
  // Get origin from request
  const origin = req.headers.origin;
  
  // Set CORS headers with explicit origin
  if (allowedOrigins.includes(origin)) {
    console.log(`Setting CORS headers for allowed origin: ${origin}`);
    res.setHeader('Access-Control-Allow-Origin', origin);
  } else {
    console.log(`Origin not in allowed list: ${origin}`);
    // For testing purposes, allow the current origin anyway
    if (origin) {
      res.setHeader('Access-Control-Allow-Origin', origin);
    } else {
      res.setHeader('Access-Control-Allow-Origin', 'https://michaelditter.com');
    }
  }
  
  // Always set these CORS headers
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, Origin');
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Max-Age', '86400'); // 24 hours
  
  // Handle OPTIONS preflight request immediately
  if (req.method === 'OPTIONS') {
    console.log('Responding to OPTIONS request with 200 OK');
    return res.status(200).end();
  }

  // Only allow POST requests for processing
  if (req.method !== 'POST') {
    console.log(`Rejecting ${req.method} request - only POST is allowed`);
    return res.status(405).json({ 
      error: 'Method not allowed', 
      message: 'Only POST requests are allowed' 
    });
  }

  try {
    // Get email from request body
    console.log(`Request body: ${JSON.stringify(req.body || {})}`);
    const { email } = req.body || {};

    // Validate email
    if (!email || !email.includes('@')) {
      console.log('Invalid email provided');
      return res.status(400).json({ 
        error: 'Invalid email', 
        message: 'Please provide a valid email address' 
      });
    }

    // No actual subscription, just return success
    console.log(`Successful test request for: ${email}`);
    return res.status(200).json({ 
      success: true, 
      message: 'This is a test endpoint. Your request was successful!',
      emailReceived: email,
      origin: origin || 'No origin header'
    });
  } catch (error) {
    console.error(`Error in test endpoint: ${error.message}`);
    return res.status(500).json({ 
      error: 'Server error', 
      message: 'Something went wrong on the server',
      details: error.message
    });
  }
} 