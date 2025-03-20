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
    
    // Read markdown file
    const markdownContent = await readFile(markdownPath, 'utf8');
    
    // Convert markdown to PDF
    return new Promise((resolve, reject) => {
      markdownpdf()
        .from.string(markdownContent)
        .to.buffer((err, buffer) => {
          if (err) reject(err);
          else resolve(buffer);
        });
    });
  } catch (error) {
    console.error('Error generating PDF:', error);
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
  if (!transporter) {
    console.warn('Email transporter not configured. Skipping email send.');
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
  
  return transporter.sendMail(mailOptions);
}

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
    
    // Generate PDF from markdown
    let pdfBuffer = null;
    let emailResult = { skipped: true };
    
    try {
      // Path to the markdown file
      const markdownPath = path.join(process.cwd(), 'public', 'AI_Marketing_FAQ.md');
      
      // Generate PDF
      pdfBuffer = await generatePdf(markdownPath);
      
      // Send email with PDF
      emailResult = await sendEmailWithPdf(email, pdfBuffer);
      
      console.log('Email sent:', emailResult);
    } catch (pdfError) {
      console.error('Error with PDF or email:', pdfError);
      // Continue with the flow even if PDF generation or email fails
    }

    // Success response
    return res.status(201).json({ 
      success: true, 
      message: 'Successfully subscribed to the newsletter! Thank you for joining.',
      emailSent: !emailResult.skipped
    });
  } catch (error) {
    console.error('Subscription error:', error);
    return res.status(500).json({ 
      error: 'Subscription failed', 
      message: 'There was an issue subscribing to the newsletter. Please try again later.' 
    });
  }
} 