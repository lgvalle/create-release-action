#!/bin/bash

current_branch=$1

if [ -z "$current_branch" ]; then
  echo "Error: Missing current branch name." >&2
  exit 1
fi

# Determine the default branch
default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | awk -F/ '{print $NF}')
if [ -z "$default_branch" ]; then
  echo "Error: Failed to determine the default branch." >&2
  exit 2
fi

# Function to get the tagger date of a tag
get_tagger_date() {
  git show -s --format="%ci" $1 2>/dev/null
}

# Get a list of all tags sorted by tagger date
tags_sorted_by_date=$(git tag --sort='-creatordate')

# Find the previous tag based on the tagger date
previous_tag=""
for tag in $tags_sorted_by_date; do
  branch_contains_tag=$(git branch --contains $tag | grep -q "$current_branch" && echo "yes" || echo "no")
  if [ "$branch_contains_tag" == "yes" ]; then
    previous_tag=$tag
    break
  fi
done

if [ -z "$previous_tag" ]; then
  echo "No previous tag found for branch $current_branch. Comparing with the default branch ($default_branch)."
  previous_tag=$default_branch
fi

# Calculate the commit log
git_command="git log $previous_tag..$current_branch --pretty=format:\"%h - %an - %ad - %s\" --date=default"
echo "Executing git command: $git_command"
commit_log=$(eval $git_command)

echo "$commit_log"
