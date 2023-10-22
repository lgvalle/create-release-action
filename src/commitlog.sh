#!/bin/bash

current_branch=$1

# Define the git format
commit_log_format="--pretty=format:\"%h - %ad - %an - %s\n\" --date=format:'%d %b %Y'"

if [ -z "$current_branch" ]; then
  echo "Error: Missing current branch name." >&2
  exit 1
fi

# Get a list of all tags sorted by tagger date
tags_sorted_by_date=$(git tag --sort='-creatordate')

# Define the git commands
git_current_commit="$(git rev-parse $current_branch)"

# Find the previous tag based on the tagger date
previous_tag=""

for tag in $tags_sorted_by_date; do
  tag_commit="$(git rev-parse $tag)"
  if [ "$tag_commit" != "$git_current_commit" ]; then
    previous_tag=$tag
    break
  fi
done


# Calculate the commit log
if [ -z "$previous_tag" ]; then
  git_command="git log $commit_log_format"
else
  git_command="git log $previous_tag..$current_branch $commit_log_format"
fi

commit_log=$(eval $git_command)

echo "$commit_log"
