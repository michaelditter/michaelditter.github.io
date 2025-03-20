# AI Research API

This is a serverless API that provides AI research data for the AI Research Index Generator. It's designed to be deployed to Vercel or a similar serverless platform.

## Features

- Serves structured AI research data across multiple categories
- Implements caching to reduce load and improve performance
- Includes rate limiting to prevent abuse
- Optional API key authentication
- CORS support for cross-origin requests
- Built-in error handling

## Deployment to Vercel

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy the API**:
   ```bash
   cd ai-research-api
   vercel
   ```

4. **Set Environment Variables** (optional):
   - `API_KEY`: For authentication (if enabled)
   - `REQUIRE_API_KEY`: Set to "true" to require API key authentication
   - `NODE_ENV`: Set to "production" for production environment

5. **Production Deployment**:
   ```bash
   vercel --prod
   ```

## API Endpoints

### GET /api/research-data

Returns the latest AI research data across multiple categories.

#### Headers

- `Authorization: Bearer YOUR_API_KEY` (optional, if API key authentication is enabled)

#### Response

```json
{
  "AI Model Updates": [
    {
      "title": "Example AI Model Update",
      "summary": "A summary of the update",
      "description_md": "Optional markdown description",
      "link": "https://example.com/article",
      "date": "2023-04-15",
      "image_url": "https://example.com/image.jpg",
      "tags": ["Tag1", "Tag2"]
    }
  ],
  "Hardware Advancements": [
    // ...
  ],
  // Additional categories
}
```

## Enhancement Options

The current implementation serves static data with dynamic dates. To enhance it:

1. **Connect to Real APIs**: Uncomment and implement the data fetching logic to retrieve real-time data from sources like arXiv, tech blogs, and news APIs.

2. **Add Database Integration**: Store and retrieve data from a database like MongoDB Atlas or Supabase.

3. **Implement Advanced Filtering**: Add query parameters to filter results by date, category, or tags.

4. **Set Up Automatic Data Collection**: Create a separate scheduled function that collects and stores data regularly.

## Local Development

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Test the API locally**:
   Uncomment the local testing code at the bottom of `api/research-data.js` and run:
   ```bash
   node api/research-data.js
   ```

3. **Use Vercel Dev**:
   ```bash
   vercel dev
   ```

## Security Considerations

- API keys are securely stored as environment variables
- Rate limiting prevents abuse
- Input validation is performed on all requests
- No sensitive operations are exposed via the API 