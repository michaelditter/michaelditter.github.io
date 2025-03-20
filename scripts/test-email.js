/**
 * Test script for email sending
 * 
 * Run with: node scripts/test-email.js
 */

// Load environment variables from .env file
require('dotenv').config();

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

// Test email to use
const TEST_EMAIL = process.env.TEST_EMAIL || 'your-test-email@example.com';

// Create a test PDF buffer (simple text file)
const testPdfBuffer = Buffer.from('This is a test PDF content for email testing', 'utf-8');

// Create transporter with the same configuration from the API
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: Number(process.env.SMTP_PORT) || 587,
  secure: process.env.SMTP_SECURE !== 'false',
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

// Email options
const mailOptions = {
  from: `"${process.env.EMAIL_FROM_NAME || 'Michael J Ditter'}" <${process.env.SMTP_USER}>`,
  to: TEST_EMAIL,
  subject: 'Test Email with PDF Attachment',
  text: 'This is a test email to verify the email sending functionality.',
  html: `
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
      <h2>Test Email</h2>
      <p>This is a test email to verify that the email sending functionality is working correctly.</p>
      <p>A test PDF is attached to this email.</p>
      <p>If you received this email, the email configuration is working!</p>
    </div>
  `,
  attachments: [
    {
      filename: 'test-attachment.pdf',
      content: testPdfBuffer
    }
  ]
};

// Log settings being used (without showing the password)
console.log('Email settings:');
console.log('- SMTP_HOST:', process.env.SMTP_HOST);
console.log('- SMTP_PORT:', process.env.SMTP_PORT);
console.log('- SMTP_SECURE:', process.env.SMTP_SECURE);
console.log('- SMTP_USER:', process.env.SMTP_USER);
console.log('- EMAIL_FROM_NAME:', process.env.EMAIL_FROM_NAME);
console.log('- Sending test email to:', TEST_EMAIL);

// Send the test email
transporter.sendMail(mailOptions)
  .then(info => {
    console.log('Email sent successfully!');
    console.log('Message ID:', info.messageId);
    console.log('Response:', info.response);
    process.exit(0);
  })
  .catch(error => {
    console.error('Error sending email:', error);
    process.exit(1);
  }); 