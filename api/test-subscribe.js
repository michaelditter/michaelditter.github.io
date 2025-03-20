// Simple test API endpoint with hardcoded CORS headers
export default async function handler(req, res) {
  // Set CORS headers with no conditions
  res.setHeader('Access-Control-Allow-Origin', 'https://michaelditter.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, Origin');
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  
  console.log(`Incoming request: ${req.method} ${req.url || ''}`);
  console.log(`Origin: ${req.headers.origin || 'unknown'}`);
  
  // Handle OPTIONS preflight request
  if (req.method === 'OPTIONS') {
    console.log('Handling OPTIONS preflight request - responding with 200 OK');
    return res.status(200).end();
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
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
      return res.status(400).json({ 
        error: 'Invalid email', 
        message: 'Please provide a valid email address' 
      });
    }

    // Just return success for testing
    return res.status(200).json({ 
      success: true, 
      message: 'This is a test endpoint. Your request was successful!',
      emailReceived: email
    });
  } catch (error) {
    console.error(`Error in test endpoint: ${error.message}`);
    return res.status(500).json({ 
      error: 'Server error', 
      message: 'Something went wrong on the server' 
    });
  }
} 