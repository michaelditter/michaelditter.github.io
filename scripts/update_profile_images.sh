#!/bin/bash

# Script to update all profile image references across the site
# Changes references from michael-ditter-headshot.jpg to michael-ditter-headshot-new.jpg

echo "Updating profile image references across the site..."

# Find all HTML files with the old image reference and update them
find . -type f -name "*.html" -exec sed -i '' 's|/img/profile/michael-ditter-headshot.jpg|/img/profile/michael-ditter-headshot-new.jpg|g' {} \;

# Make sure the new image file exists and has content
if [ ! -s "img/profile/michael-ditter-headshot-new.jpg" ]; then
  echo "Warning: The new image file is empty or doesn't exist. Copying from the original..."
  cp img/profile/michael-ditter-headshot.jpg img/profile/michael-ditter-headshot-new.jpg
fi

echo "Profile image references updated successfully!" 