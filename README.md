# Auto Release Action

This GitHub Action automatically creates a new release in Github when a given branch is merged.
The description of the release contains the list of commits since the last tag


```yaml
name: Create Release

on:
  pull_request:
    branches:
      - main
    types: 
      - closed

jobs:      
  create_release:
    runs-on: ubuntu-latest
    if: startsWith(github.head_ref, 'release/') && github.event.pull_request.merged == true
    steps:
      - uses: actions/checkout@v4
      - name: Create Release action
        uses: lgvalle/create-release-action@release/v0.4.3
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

* `openai-api-key` is an optional parameter. If present, it will create a summary a human-readable summary of the changelog