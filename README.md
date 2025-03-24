# Michael Ditter Website with Bitcoin and AI Reports

This project contains Michael Ditter's personal website with enhanced real-time Bitcoin reports and interactive AI visualizations using Shadcn UI components.

## 🚀 One-Click Deployment

### Option 1: Deploy via Script (Recommended)

1. **Simply run the deployment script**:
   ```bash
   ./deploy.sh
   ```
   This script will:
   - Initialize a Git repository (if needed)
   - Add and commit all files
   - Guide you through connecting to your GitHub
   - Push everything to your repository
   - Provide step-by-step instructions for importing to Replit

### Option 2: Manual Deployment

If you prefer to deploy manually:

1. **Create a GitHub repository**:
   - Go to [GitHub.com](https://github.com/new)
   - Create a new repository (e.g., `michael-ditter-website`)

2. **Connect and push your local code**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit with Bitcoin and AI reports"
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## 🛠️ Import to Replit

1. Go to [Replit](https://replit.com) and sign in
2. Click the "+ Create" button
3. Select "Import from GitHub"
4. Paste your repository URL
5. Choose "HTML, CSS, JS" as the language preset
6. Click "Import from GitHub"

The setup will run automatically thanks to the included setup scripts. Just click "Run" in Replit once it's imported!

## ✨ Features

- **Real-time Bitcoin Data**: Displays current Bitcoin price, market data, and insights with automatic updates
- **Interactive AI Report Charts**: Visualizes ChatGPT's dominance in India using Chart.js
- **Shadcn UI Components**: Modern, responsive user interface with sleek design
- **Replit-Ready Configuration**: Automatic setup in Replit environment

## 🏗️ Project Structure

```
/
├── index.html             # Main website HTML
├── css/                   # CSS styling files
│   └── custom-overrides.css  # Bitcoin and AI report styles
├── js/                    # JavaScript files
│   └── main.js            # Bitcoin data fetching and chart rendering
├── bitcoin-research-api/  # Bitcoin data API
│   └── api/
│       └── bitcoin-data.js  # Sample Bitcoin data endpoint
├── deploy.sh              # Deployment script
├── replit-setup.js        # Replit initialization script
└── .replit                # Replit configuration
```

## 📝 Customization

- **Bitcoin Data**: Modify `js/main.js` to change how Bitcoin data is fetched and displayed
- **AI Charts**: Update the chart configurations in `js/main.js` to adjust the ChatGPT report charts
- **Styling**: Customize the appearance in `css/custom-overrides.css`

## 🤔 Troubleshooting

If you encounter any issues in Replit:
1. Check the console for errors (F12 or right-click > Inspect > Console)
2. Verify that the server is running correctly
3. Make sure all dependencies are installed
4. Try running `npm run setup` manually

## 📄 License

MIT License - See LICENSE file for details 