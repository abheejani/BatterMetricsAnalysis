#!/bin/bash

# Set the size limit just below the LFS 2 GB limit (1900M is approx 1.9 GB)
LIMIT=1900M

# Find all files larger than the limit in your working directory (ignoring .git folder)
find . -type f -size +1900M -not -path "./.git/*" | while read FILE; do
    # Get the base name without directory structure
    BASENAME=$(basename "$FILE")
    echo "Splitting $FILE into parts..."
    
    # Split the file into chunks with the specified limit
    split -b $LIMIT "$FILE" "${FILE}_part_"
    
    # Remove the original large file from git and LFS
    git rm --cached "$FILE"
    
    # Add the split parts to git
    git add "${FILE}_part_*"
done

# Commit the changes after splitting
git commit -m "Split large files into smaller chunks for upload"
