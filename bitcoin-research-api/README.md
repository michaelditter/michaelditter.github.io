# Bitcoin Research API

This is a serverless API that provides Bitcoin research data. It's designed to be deployed to Vercel or a similar serverless platform.

## Features

- Provides Bitcoin market data, price analysis, and research insights
- In-memory caching to improve performance
- Rate limiting to prevent abuse
- CORS support for cross-origin requests
- Optional API key authentication

## Deployment

### Deploy to Vercel

1. Install the Vercel CLI if you don't have it:
   ```
   npm install -g vercel
   ```

2. Login to Vercel:
   ```
   vercel login
   ```

3. Deploy the API:
   ```
   vercel
   ```

4. For production deployment:
   ```
   vercel --prod
   ```

### Environment Variables

You can configure the API by setting the following environment variables in Vercel:

- `API_KEY`: Set this to a secure random string if you want to enable API key authentication
- `REQUIRE_API_KEY`: Set to "true" to require API key authentication, "false" to disable
- `NODE_ENV`: Set to "production" for production deployments

## Usage

Once deployed, you can access the API at:

```
https://your-vercel-app-name.vercel.app/api/bitcoin-data
```

If API key authentication is enabled, include the API key in the Authorization header:

```
Authorization: Bearer your-api-key
```

## Local Development

1. Install dependencies:
   ```
   npm install
   ```

2. Run the development script:
   ```
   npm run dev
   ```

3. For local Vercel development:
   ```
   npm start
   ```

## Response Format

The API returns Bitcoin research data in JSON format with the following structure:

```json
{
  "reportDate": "2023-06-09",
  "bitcoinPrice": {
    "current": "$84,570",
    "weeklyChange": "2.5%",
    "weeklyTrend": "up"
  },
  "marketSummary": {
    "marketCap": "$1.65 trillion",
    "volume24h": "$45.2 billion",
    "dominance": "57.2%"
  },
  "keyInsights": [
    {
      "title": "Institutional Adoption Accelerates",
      "content": "Major financial institutions including Fidelity and BlackRock continue to increase their Bitcoin holdings.",
      "source": "Bloomberg Financial",
      "date": "2023-06-07"
    },
    // ...more insights
  ],
  // ...other sections
}
```

## Integration with GitHub Actions

This API is designed to be used with the Bitcoin Research Index Generator that runs on a scheduled GitHub Action. The generator fetches data from this API and creates a static HTML report. 