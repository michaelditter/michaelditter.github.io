// Vercel serverless function for newsletter subscription
// This API endpoint handles newsletter subscriptions via Buttondown

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight requests for CORS
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed', message: 'Only POST requests are allowed' });
  }

  try {
    // Get email from request body
    const { email } = req.body;

    // Validate email
    if (!email || !email.includes('@')) {
      return res.status(400).json({ error: 'Invalid email', message: 'Please provide a valid email address' });
    }

    // Get API key from environment variable
    const apiKey = process.env.BUTTONDOWN_API_KEY;
    if (!apiKey) {
      console.error('BUTTONDOWN_API_KEY is not set');
      return res.status(500).json({ error: 'Server configuration error', message: 'Newsletter service is not properly configured' });
    }

    // Call Buttondown API to add subscriber
    const response = await fetch('https://api.buttondown.email/v1/subscribers', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });

    // Parse response
    const data = await response.json();

    // Check for errors
    if (!response.ok) {
      // If the email is already subscribed, return a more friendly message
      if (response.status === 400 && data.email && data.email[0] === 'This email address is already subscribed.') {
        return res.status(400).json({ 
          error: 'Already subscribed', 
          message: 'This email is already subscribed to the newsletter. Thank you for your interest!' 
        });
      }

      console.error('Buttondown API error:', data);
      throw new Error(data.error || 'Failed to subscribe');
    }

    // Success response
    return res.status(201).json({ 
      success: true, 
      message: 'Successfully subscribed to the newsletter! Thank you for joining.' 
    });
  } catch (error) {
    console.error('Subscription error:', error);
    return res.status(500).json({ 
      error: 'Subscription failed', 
      message: 'There was an issue subscribing to the newsletter. Please try again later.' 
    });
  }
} 