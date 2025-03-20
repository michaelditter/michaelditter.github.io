# Secure API Key Management Guide

This guide outlines best practices for managing API keys securely in your research index generators.

## General Security Principles

1. **Never commit API keys to version control**
2. **Use environment variables** or secure vaults to store keys
3. **Rotate keys periodically** (every 90 days is recommended)
4. **Use least privilege** - keys should only have access to what they need
5. **Monitor key usage** for unusual activity

## API Key Storage Options

### 1. Environment Variables (Local Development)

For local development, use `.env` files:

```bash
# .env file (add to .gitignore)
AI_RESEARCH_API_KEY=your_secret_key_here
BITCOIN_RESEARCH_API_KEY=your_secret_key_here
```

Load keys in your scripts:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env
api_key = os.getenv("AI_RESEARCH_API_KEY")
```

### 2. GitHub Secrets (CI/CD)

For GitHub Actions workflows:

1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add your API keys:
   - Name: `AI_RESEARCH_API_KEY`
   - Value: `your_secret_key_here`
5. Repeat for `BITCOIN_RESEARCH_API_KEY`

Reference secrets in workflows:
```yaml
env:
  API_KEY: ${{ secrets.AI_RESEARCH_API_KEY }}
```

### 3. Vercel Environment Variables (API Deployment)

For Vercel-deployed APIs:

1. Go to your Vercel project
2. Navigate to Settings → Environment Variables
3. Add your production keys:
   - Name: `API_KEY`
   - Value: `your_secret_key_here`
   - Environment: Production

### 4. Key Rotation Process

1. Generate a new key in the service provider's console
2. Update the key in all storage locations
3. Test that everything works with the new key
4. Deprecate the old key
5. After a testing period, delete the old key

### 5. What To Do If Keys Are Exposed

If you suspect an API key has been compromised:

1. Immediately rotate the key (generate a new one and delete the old one)
2. Review service logs for unauthorized access
3. Check for unexpected charges or usage
4. Update all locations where the key is stored
5. Review your code and workflows to prevent future exposure

## Production API Key Requirements

The research generators require these API keys in production:

1. **AI Research API Key**
   - Purpose: Access OpenAI API for AI research data generation
   - Required by: `.github/workflows/ai-research-update.yml`, `.github/workflows/ai-content-generator.yml`, `.github/workflows/bitcoin-newsletter.yml`
   - Storage: GitHub Secrets as `OPENAI_API_KEY`

2. **Bitcoin Research API Key**
   - Purpose: Access Bitcoin research data API
   - Required by: `.github/workflows/bitcoin-research-update.yml`
   - Storage: GitHub Secrets as `BITCOIN_RESEARCH_API_KEY`
   - Note: The environment variable is referenced as `API_KEY_ENV: "BITCOIN_RESEARCH_API_KEY"` in the generator code

3. **Vercel API Keys** (If using API key authentication)
   - Purpose: Authenticate requests to your serverless APIs
   - Required by: Bitcoin and AI Research APIs
   - Storage: Vercel Environment Variables as follows:
     - `BUTTONDOWN_API_KEY`: Newsletter subscription service
     - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`: Email delivery settings
     - `SMTP_SECURE`: Boolean for secure email connection
     - `EMAIL_FROM_NAME`: Name to show in newsletter emails 