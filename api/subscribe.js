// Vercel serverless function for newsletter subscription
// This API endpoint handles newsletter subscriptions via Buttondown
// It also generates a PDF from Markdown and emails it to new subscribers

import fs from 'fs';
import path from 'path';
import nodemailer from 'nodemailer';
import markdownpdf from 'markdown-pdf';
import { promisify } from 'util';

// Promisify fs.readFile
const readFile = promisify(fs.readFile);
const access = promisify(fs.access);

// Enhanced logging helper with timestamps
const log = (message) => {
  console.log(`[${new Date().toISOString()}] [subscribe] ${message}`);
};

// Log environment variables presence (without exposing values)
log(`Environment variables available: ${Object.keys(process.env).filter(key => 
  key.includes('BUTTONDOWN') || 
  key.includes('SMTP') || 
  key.includes('EMAIL')
).join(', ')}`);
log(`BUTTONDOWN_API_KEY present? ${!!process.env.BUTTONDOWN_API_KEY}`);
log(`SMTP configuration present? ${!!(process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASS)}`);

// Configure email transporter
let transporter = null;
if (process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASS) {
  transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: Number(process.env.SMTP_PORT) || 587,
    secure: process.env.SMTP_SECURE !== 'false', // true for 465, false for other ports
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS
    },
    // Microsoft Office365/Outlook specific configuration
    tls: {
      ciphers: 'SSLv3',
      rejectUnauthorized: false
    }
  });
  log(`Email transporter configured with host: ${process.env.SMTP_HOST}, port: ${process.env.SMTP_PORT || 587}`);
} else {
  log('Email transporter not configured - missing environment variables');
}

/**
 * Generate PDF from Markdown file
 * @param {string} markdownPath - Path to the markdown file
 * @returns {Promise<Buffer>} - PDF file as buffer
 */
async function generatePdf(markdownPath) {
  try {
    // Check if markdown file exists
    await access(markdownPath, fs.constants.R_OK);
    log(`Markdown file found at ${markdownPath}`);
    
    // Read markdown file
    const markdownContent = await readFile(markdownPath, 'utf8');
    log(`Read markdown content (${markdownContent.length} bytes)`);
    
    // Convert markdown to PDF
    return new Promise((resolve, reject) => {
      log('Starting PDF generation from markdown');
      markdownpdf()
        .from.string(markdownContent)
        .to.buffer((err, buffer) => {
          if (err) {
            log(`Error generating PDF: ${err.message}`);
            console.error('[subscribe] PDF generation error:', err.stack || err);
            reject(err);
          } else {
            log(`Generated PDF successfully (${buffer.length} bytes)`);
            resolve(buffer);
          }
        });
    });
  } catch (error) {
    log(`Error in generatePdf: ${error.message}`);
    console.error('[subscribe] Generate PDF error stack:', error.stack || error);
    throw error;
  }
}

/**
 * Send email with PDF attachment
 * @param {string} to - Recipient email
 * @param {Buffer} pdfBuffer - PDF file as buffer
 * @returns {Promise<object>} - Email send result
 */
async function sendEmailWithPdf(to, pdfBuffer) {
  try {
    if (!transporter) {
      log('Email transporter not configured. Skipping email send.');
      return { skipped: true, reason: 'Email transporter not configured' };
    }
    
    const mailOptions = {
      from: `"${process.env.EMAIL_FROM_NAME || 'Michael J Ditter'}" <${process.env.SMTP_USER}>`,
      to,
      subject: 'Your AI Marketing FAQ PDF',
      text: 'Thank you for subscribing to my newsletter! Please find attached the AI Marketing FAQ PDF guide.',
      html: `
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
          <h2>Thank you for subscribing!</h2>
          <p>I'm excited to share insights on AI, emerging technologies, and digital innovation with you.</p>
          <p>As promised, here's your <strong>AI Marketing FAQ</strong> guide (attached as a PDF).</p>
          <p>You'll start receiving my newsletter with the latest content and updates.</p>
          <p>Best regards,<br>Michael J Ditter</p>
        </div>
      `,
      attachments: [
        {
          filename: 'AI-Marketing-FAQ.pdf',
          content: pdfBuffer
        }
      ]
    };
    
    log(`Sending email to ${to} with attachment (${pdfBuffer.length} bytes)`);
    const result = await transporter.sendMail(mailOptions);
    log(`Email sent successfully - messageId: ${result.messageId}`);
    return result;
  } catch (emailError) {
    log(`Error sending email: ${emailError.message}`);
    console.error('[subscribe] Email sending error:', emailError.stack || emailError);
    throw emailError;
  }
}

// Export handler function
export default async function handler(req, res) {
  log('=============== Function invoked ===============');
  log(`Request method: ${req.method}`);
  log(`Request URL: ${req.url}`);
  
  // ============ CORS HANDLING - ENHANCED VERSION ============
  // Get the origin from the request
  const origin = req.headers.origin;
  log(`Request origin: ${origin || 'unknown'}`);
  
  // Define allowed origins
  const allowedOrigins = [
    'https://michaelditter.github.io', 
    'https://michaelditter.com', 
    'https://www.michaelditter.com',
    'https://michael-ditter-branding.vercel.app',
    'https://api-only-pq88ssbko-michael-ditters-projects.vercel.app',
    'http://localhost:3000'
  ];
  
  // Set CORS headers - Allow requests from allowed origins
  if (allowedOrigins.includes(origin)) {
    log(`Origin ${origin} is allowed - setting CORS headers`);
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, Origin');
    res.setHeader('Access-Control-Max-Age', '86400'); // 24 hours
  } else {
    log(`WARNING: Request from non-allowed origin: ${origin}`);
    // Fall back to default origin for development/testing
    res.setHeader('Access-Control-Allow-Origin', '*'); // Temporarily allow all origins for debugging
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, Origin');
  }
  
  // Handle OPTIONS (preflight) request immediately
  if (req.method === 'OPTIONS') {
    log('Handling OPTIONS preflight request - responding with 200 OK');
    return res.status(200).end();
  }
  
  // Log request headers (safely)
  const safeHeaders = { ...req.headers };
  if (safeHeaders.authorization) safeHeaders.authorization = '[REDACTED]';
  log(`Headers: ${JSON.stringify(safeHeaders)}`);
  
  // ============ END CORS HANDLING ============

  // Only allow POST requests for actual processing
  if (req.method !== 'POST') {
    log(`Method not allowed: ${req.method}`);
    return res.status(405).json({ error: 'Method not allowed', message: 'Only POST requests are allowed' });
  }

  try {
    // Get email from request body
    const bodyData = req.body || {};
    log(`Request body: ${JSON.stringify(bodyData)}`);
    const email = bodyData.email_address;

    // Validate email
    if (!email || !email.includes('@')) {
      log('Invalid email provided');
      return res.status(400).json({ error: 'Invalid email', message: 'Please provide a valid email address' });
    }

    log(`Processing subscription for email: ${email}`);

    // Get API key from environment variable
    const apiKey = process.env.BUTTONDOWN_API_KEY;
    if (!apiKey) {
      log('BUTTONDOWN_API_KEY is not set');
      return res.status(500).json({ error: 'Server configuration error', message: 'Newsletter service is not properly configured' });
    }

    // Call Buttondown API to add subscriber
    log('Calling Buttondown API');
    try {
      const response = await fetch('https://api.buttondown.email/v1/subscribers', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email_address: email }),
      });

      log(`Buttondown API response status: ${response.status}`);
      
      // Get response text first for logging
      const responseText = await response.text();
      log(`Buttondown API response text: ${responseText}`);
      
      // Parse JSON if possible
      let data;
      try {
        data = JSON.parse(responseText);
        log(`Buttondown API parsed response: ${JSON.stringify(data)}`);
      } catch (parseError) {
        log(`Could not parse Buttondown response as JSON: ${parseError.message}`);
        data = { error: 'Invalid response format' };
      }

      // Check for errors
      if (!response.ok) {
        // If the email is already subscribed, return a more friendly message
        if (response.status === 400 && data.email_address && 
            Array.isArray(data.email_address) && 
            data.email_address[0].includes("already subscribed")) {
          log('Email already subscribed');
          return res.status(400).json({ 
            error: 'Already subscribed', 
            message: 'This email is already subscribed to the newsletter. Thank you for your interest!' 
          });
        }

        log(`Buttondown API error: ${JSON.stringify(data)}`);
        throw new Error(data.error || `Failed to subscribe (Status: ${response.status})`);
      }
    } catch (apiError) {
      log(`Error calling Buttondown API: ${apiError.message}`);
      console.error('[subscribe] Buttondown API error:', apiError.stack || apiError);
      throw apiError;
    }
    
    // Generate PDF from markdown
    let pdfBuffer = null;
    let emailResult = { skipped: true };
    
    try {
      // Path to the markdown file
      const markdownPath = path.join(process.cwd(), 'public', 'AI_Marketing_FAQ.md');
      log(`Attempting to generate PDF from ${markdownPath}`);
      
      // Generate PDF
      pdfBuffer = await generatePdf(markdownPath);
      log(`PDF generated successfully (${pdfBuffer?.length || 0} bytes)`);
      
      // Send email with PDF
      emailResult = await sendEmailWithPdf(email, pdfBuffer);
      
      log(`Email sent result: ${JSON.stringify(emailResult)}`);
    } catch (pdfError) {
      log(`Error with PDF or email: ${pdfError.message}`);
      console.error('[subscribe] PDF/Email error stack:', pdfError.stack || pdfError);
      // Continue with the flow even if PDF generation or email fails
    }

    // Success response
    log('Subscription successful');
    return res.status(201).json({ 
      success: true, 
      message: 'Successfully subscribed to the newsletter! Thank you for joining.',
      emailSent: !emailResult.skipped
    });
  } catch (error) {
    log(`Subscription error: ${error.message}`);
    console.error('[subscribe] Full error stack:', error.stack || error);
    return res.status(500).json({ 
      error: 'Subscription failed', 
      message: 'There was an issue subscribing to the newsletter. Please try again later.',
      details: error.message
    });
  } finally {
    log('=============== Function completed ===============');
  }
} 