# Newsletter Subscription System Setup Guide

This guide explains how to set up and deploy the newsletter subscription system with PDF delivery for Michael Ditter's website.

## System Overview

The newsletter subscription system includes:

1. **Signup Forms**: Located in the hero section and throughout blog posts
2. **PDF Generation**: Converts Markdown FAQ to a PDF on-the-fly
3. **Email Delivery**: Sends the PDF to new subscribers
4. **Buttondown Integration**: Adds subscribers to your newsletter service

## Installation and Setup

### 1. Install Dependencies

The system requires Node.js dependencies for PDF generation and email sending:

```bash
npm install
```

This will install:
- markdown-pdf (for converting Markdown to PDF)
- nodemailer (for sending emails)
- dotenv (for loading environment variables)

### 2. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Update the following variables:

```
# Buttondown API key (get from Buttondown settings)
BUTTONDOWN_API_KEY=your_buttondown_api_key_here

# Email configuration (SMTP)
SMTP_HOST=smtp.example.com
SMTP_PORT=465
SMTP_SECURE=true
SMTP_USER=your_email@example.com
SMTP_PASS=your_email_password_or_app_password
EMAIL_FROM_NAME=Michael J Ditter
```

For Gmail, you can use:
- SMTP_HOST=smtp.gmail.com
- SMTP_PORT=465
- SMTP_USER=your.email@gmail.com
- SMTP_PASS=your_app_password (Create an app password in Google Account settings)

### 3. Update AI Marketing FAQ Content

The FAQ content is located in `public/AI_Marketing_FAQ.md`. You can update this file to change the content of the PDF that subscribers receive.

### 4. Local Testing

To test the system locally:

```bash
# Run a local web server
npm run dev

# Test the API with curl
curl -X POST -H "Content-Type: application/json" -d '{"email":"test@example.com"}' http://localhost:3000/api/subscribe
```

Check your email to verify PDF delivery.

## Deployment

### 1. Deploy to Vercel

The system is designed to work with Vercel:

```bash
vercel
```

When deploying to production:

```bash
vercel --prod
```

### 2. Configure Vercel Environment Variables

In the Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add all variables from your `.env` file
4. Make sure to use Vercel Secrets for sensitive information:

```bash
vercel secret add buttondown_api_key "your_api_key"
vercel secret add smtp_pass "your_smtp_password"
```

Then update the `vercel.json` file to reference these secrets.

### 3. Verify Deployment

After deployment:

1. Test the subscribe form on your live site
2. Verify that subscribers are added to Buttondown
3. Check that the PDF is delivered to subscribers' emails

## Troubleshooting

### Email Delivery Issues

If emails aren't being sent:

1. Check SMTP credentials
2. Verify that environment variables are correctly set
3. Look at Vercel function logs for error messages

For Gmail users:
- Ensure you're using an App Password, not your regular password
- Check if "Less secure app access" needs to be enabled

### PDF Generation Issues

If PDFs aren't generating:

1. Verify that `public/AI_Marketing_FAQ.md` exists and is formatted correctly
2. Check for error messages in the Vercel logs
3. Try running the PDF generation locally to debug

### Buttondown API Issues

If subscribers aren't being added to Buttondown:

1. Verify your API key is correct
2. Check if you have a paid Buttondown account (API access requires a paid tier)
3. Look for API error responses in the logs

## Future Enhancements

Potential improvements to consider:

1. Add analytics tracking for subscription conversions
2. Implement A/B testing for different PDF incentives
3. Add a custom thank-you page after subscription
4. Create a subscriber management dashboard
5. Set up automated follow-up email sequences 