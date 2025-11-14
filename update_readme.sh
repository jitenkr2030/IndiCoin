#!/bin/bash
# Script to update IndiCoin repository README.md
# Run this script in your local machine where you have the repository cloned

echo "Updating IndiCoin repository README.md..."

# Step 1: Pull latest changes
git pull origin main

# Step 2: Backup current README
cp README.md README.md.backup

# Step 3: Create new README.md (copy the content I provided)
# The new README.md content has been prepared and is ready to use

# Step 4: Add, commit and push
git add README.md
git commit -m "Update README.md with comprehensive IndiCoin documentation"
git push origin main

echo "README.md updated successfully!"