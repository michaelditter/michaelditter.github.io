#!/bin/bash

# Deploy.sh - Automated Git deployment script for Michael Ditter Website
# Run this script to automatically initialize and push to GitHub

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install Git first."
    exit 1
fi

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Michael Ditter Website Deployment Script ===${NC}"

# Check if it's already a git repository
if [ -d .git ]; then
    echo -e "${GREEN}Git repository already initialized.${NC}"
else
    echo "Initializing Git repository..."
    git init
    echo -e "${GREEN}Git repository initialized.${NC}"
fi

# Add all files to Git
echo "Adding files to Git..."
git add .
echo -e "${GREEN}Files added to Git.${NC}"

# Commit changes
echo "Committing changes..."
git commit -m "Deploy Bitcoin and AI reports with Shadcn UI components"
echo -e "${GREEN}Changes committed.${NC}"

# Ask for GitHub username and repository name
echo -e "${BLUE}Please enter your GitHub username:${NC}"
read github_username

echo -e "${BLUE}Please enter the repository name (e.g., michael-ditter-website):${NC}"
read repo_name

# Configure remote
echo "Setting up GitHub remote..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$github_username/$repo_name.git"
echo -e "${GREEN}GitHub remote configured.${NC}"

# Push to GitHub
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main
push_status=$?

if [ $push_status -eq 0 ]; then
    echo -e "${GREEN}Successfully pushed to GitHub!${NC}"
    echo -e "${BLUE}=== Next Steps ===${NC}"
    echo -e "1. Your code is now on GitHub at: ${GREEN}https://github.com/$github_username/$repo_name${NC}"
    echo -e "2. Go to ${GREEN}https://replit.com${NC}"
    echo -e "3. Click '+ Create' and select 'Import from GitHub'"
    echo -e "4. Paste your repository URL: ${GREEN}https://github.com/$github_username/$repo_name${NC}"
    echo -e "5. Select 'HTML, CSS, JS' as the language preset"
    echo -e "6. Click 'Import from GitHub'"
    echo -e "7. Once imported, Replit will set up your environment automatically"
    echo -e "8. Click the 'Run' button in Replit"
    echo -e "${GREEN}Your website with the Bitcoin and AI reports should now be running in Replit!${NC}"
else
    echo -e "${RED}Failed to push to GitHub. Please check your credentials and try again.${NC}"
    echo -e "You might need to create the repository first at: ${GREEN}https://github.com/new${NC}"
    echo -e "Or make sure you have the correct permissions to push to this repository."
fi 