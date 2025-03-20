# Deployment Guide for Research Index Generators

This guide provides step-by-step instructions for deploying the AI and Bitcoin Research Index Generators to production.

## Prerequisites

- GitHub account with access to the repository
- Vercel account for API deployment
- API keys for any external services used

## 1. Deploy APIs to Vercel

### Bitcoin Research API

1. Navigate to the `bitcoin-research-api` directory:
   ```bash
   cd bitcoin-research-api
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Deploy to Vercel:
   ```bash
   npx vercel login
   npx vercel
   ```

4. When prompted, follow the Vercel CLI instructions. For production deployment:
   ```bash
   npx vercel --prod
   ```

5. Note the deployment URL, you'll need it for the GitHub Actions workflow.

### AI Research API

Follow similar steps for the AI Research API if you're hosting it yourself.

## 2. Set Up GitHub Secrets

For secure API key management, add them to GitHub Secrets:

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add the following secrets:
   - `AI_RESEARCH_API_KEY`: API key for the AI Research API
   - `BITCOIN_RESEARCH_API_KEY`: API key for the Bitcoin Research API

## 3. Configure GitHub Actions Workflows

Update the API URLs in the GitHub Actions workflow files:

1. Open `.github/workflows/ai-research-update.yml` and update the `API_URL` value:
   ```yaml
   API_URL: "https://your-ai-research-api-url.vercel.app/api/research-data"
   ```

2. Open `.github/workflows/bitcoin-research-update.yml` and update the `API_URL` value:
   ```yaml
   API_URL: "https://your-bitcoin-research-api-url.vercel.app/api/bitcoin-data"
   ```

## 4. Ensure Proper Image Storage

Make sure the following directories exist for image storage:

```bash
mkdir -p img/ai-research
mkdir -p img/bitcoin-research
mkdir -p img/blog
```

Add placeholder images for the blog cards:

```bash
# Use placeholder images or create your own
cp placeholder.jpg img/blog/ai-research-index.jpg
cp placeholder.jpg img/blog/bitcoin-research-index.jpg
```

## 5. Test the Workflows Locally

Before relying on the scheduled runs, test the generators locally:

```bash
# Test AI Research Generator with file data
DATA_SOURCE_TYPE=file bash ai_research_generator/run_generator.sh

# Test Bitcoin Research Generator with file data
DATA_SOURCE_TYPE=file bash bitcoin_research_generator/run_generator.sh
```

Once the APIs are deployed, test with API data:

```bash
# Test with API data
DATA_SOURCE_TYPE=api API_URL=https://your-api-url.vercel.app/api/endpoint bash ai_research_generator/run_generator.sh
DATA_SOURCE_TYPE=api API_URL=https://your-api-url.vercel.app/api/endpoint bash bitcoin_research_generator/run_generator.sh
```

## 6. Commit and Push Changes

```bash
git add .
git commit -m "Configure for production deployment"
git push
```

## 7. Verify Scheduled Workflows

- AI Research Index will update every Wednesday at midnight UTC
- Bitcoin Research Index will update every Friday at midnight UTC

You can also trigger manual runs from the GitHub Actions tab in your repository.

## Troubleshooting

If the workflows fail:

1. Check the GitHub Actions logs for error messages
2. Verify that API keys are correctly set in GitHub Secrets
3. Confirm the API endpoints are accessible
4. Test the generators locally with the same configuration
5. Check if the APIs are returning valid data
6. Review the error handling in the generator scripts 