# Platform APIs Reference

Platform-agnostic repository API usage guide and reference.

## Overview

The create-pr skill supports multiple platforms through auto-detection:
- **GitLab/GitCode**: Uses GitLab API v4
- **GitHub**: Uses GitHub REST API v3
- **Other platforms**: Falls back to web-based PR creation

## Platform Detection

The script automatically detects the platform from your git remote URL:
```bash
git remote get-url origin
```

- `github.com` → GitHub API
- `gitcode.com` or `gitlab.com` → GitLab API v4
- Other URLs → Web interface fallback

## Authentication

### Personal Access Tokens

```bash
# For GitHub
git config --global github.token "your_token"
# Or
export GITHUB_TOKEN="your_token"

# For GitCode/GitLab
git config --global gitcode.token "your_token"
# Or
export GITCODE_TOKEN="your_token"

# Generic (works with any platform)
export REPO_TOKEN="your_token"
```

### Token Permissions

**GitHub** (`repo` scope):
- `repo` (full repository access)
- `repo:status` (commit status)
- `repo_deployment` (deployment status)

**GitLab/GitCode** (`api` scopes):
- `api` (full API access)
- `read_api` (read API resources)
- `write_repository` (write to repository)

## GitHub API

### Base URL
```
https://api.github.com
```

### Create Issue

**Endpoint**: `POST /repos/{owner}/{repo}/issues`

```bash
curl -X POST \
  -H "Authorization: Bearer your_token" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/owner/repo/issues" \
  -d '{"title": "Issue title", "body": "Issue description", "labels": ["bug"]}'
```

### Create Pull Request

**Endpoint**: `POST /repos/{owner}/{repo}/pulls`

```bash
curl -X POST \
  -H "Authorization: Bearer your_token" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/owner/repo/pulls" \
  -d '{
    "title": "PR title",
    "body": "PR description",
    "head": "feature-branch",
    "base": "main"
  }'
```

## GitLab/GitCode API

### Base URL
```
https://gitcode.com/api/v4
```

### Create Issue

**Endpoint**: `POST /projects/:id/issues`

```bash
curl -X POST \
  -H "PRIVATE-TOKEN: your_token" \
  "https://gitcode.com/api/v4/projects/owner%2Frepo/issues" \
  -d '{"title": "Issue title", "description": "Issue description"}'
```

### Create Merge Request

**Endpoint**: `POST /projects/:id/merge_requests`

```bash
curl -X POST \
  -H "PRIVATE-TOKEN: your_token" \
  "https://gitcode.com/api/v4/projects/owner%2Frepo/merge_requests" \
  -d '{
    "source_branch": "feature-branch",
    "target_branch": "main",
    "title": "MR title",
    "description": "MR description"
  }'
```

## URL Encoding

For GitLab/GitCode, the project path must be URL-encoded:
- `owner/repo` → `owner%2Frepo`
- Use `encodeURIComponent()` in JavaScript or `urllib.parse.quote()` in Python

## PR-Issue Linkage

### Via Description

Add specific keywords to automatically link PR to Issue:

```markdown
Fixes #42       # Closes issue when PR merges
Closes #42       # Same as Fixes
Resolves #42     # Same as Fixes
Related to #42   # Links but doesn't close
Refs #42         # Reference only
```

### Via API

GitHub and GitLab automatically parse these keywords from PR/MR descriptions.

## Error Handling

### Common Error Codes

| Code | GitHub | GitLab |
|------|--------|--------|
| 400 | Bad Request | Bad Request |
| 401 | Unauthorized | 401 Unauthorized |
| 403 | Forbidden | 403 Forbidden |
| 404 | Not Found | 404 Not Found |
| 409 | Conflict | 409 Conflict (MR already exists) |
| 422 | Validation Failed | 422 Unprocessable Entity |

### Error Handling in Python

```python
import urllib.error

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    print(f"HTTP Error {e.code}: {error_body}")
except Exception as e:
    print(f"Error: {e}")
```

## Rate Limits

### GitHub
- Authenticated: 5000 requests/hour
- Unauthenticated: 60 requests/hour

Check status:
```bash
curl -I -H "Authorization: token your_token" \
  https://api.github.com/users/username
```

### GitLab/GitCode
- Authenticated: 600 requests/minute
- Unauthenticated: 300 requests/minute

## Pagination

Most list APIs support pagination:

```bash
# GitHub
curl "https://api.github.com/repos/owner/repo/issues?per_page=100&page=1"

# GitLab/GitCode
curl "https://gitcode.com/api/v4/projects/owner%2Frepo/issues?per_page=100&page=1"
```

## Webhooks

### GitHub

```bash
curl -X POST \
  -H "Authorization: Bearer your_token" \
  "https://api.github.com/repos/owner/repo/hooks" \
  -d '{
    "name": "web",
    "active": true,
    "events": ["push", "pull_request"],
    "config": {"url": "https://example.com/webhook"}
  }'
```

### GitLab/GitCode

```bash
curl -X POST \
  -H "PRIVATE-TOKEN: your_token" \
  "https://gitcode.com/api/v4/projects/owner%2Frepo/hooks" \
  -d '{
    "url": "https://example.com/webhook",
    "push_events": true,
    "merge_requests_events": true
  }'
```

## Platform-Specific Notes

### GitHub
- Uses "pull requests" instead of "merge requests"
- API endpoints use `/repos/` prefix
- Project ID is `{owner}/{repo}`
- Uses `head` and `base` for branch names

### GitLab/GitCode
- Uses "merge requests"
- API endpoints use `/projects/` prefix
- Project ID is URL-encoded `{owner}%2F{repo}`
- Uses `source_branch` and `target_branch`
- Fork format: `{fork_owner}/{branch}`

## Complete Example

### Create Issue and Linked PR (GitHub)

```python
import urllib.request
import json

token = "your_token"
owner_repo = "owner/repo"
api_base = "https://api.github.com"

# 1. Create Issue
issue_data = {
    "title": "Add feature",
    "body": "## Summary\n\nAdd new feature",
    "labels": ["enhancement"]
}

req = urllib.request.Request(
    f"{api_base}/repos/{owner_repo}/issues",
    data=json.dumps(issue_data).encode('utf-8'),
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
)

with urllib.request.urlopen(req) as response:
    issue = json.loads(response.read().decode('utf-8'))
    issue_number = issue['number']
    print(f"Issue created: #{issue_number}")

# 2. Create linked PR
pr_data = {
    "title": "Add feature",
    "body": f"## Summary\n\nAdd new feature\n\nFixes #{issue_number}",
    "head": "feature-branch",
    "base": "main"
}

req = urllib.request.Request(
    f"{api_base}/repos/{owner_repo}/pulls",
    data=json.dumps(pr_data).encode('utf-8'),
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
)

with urllib.request.urlopen(req) as response:
    pr = json.loads(response.read().decode('utf-8'))
    print(f"PR created: #{pr['number']}")
```

### Create Issue and Linked MR (GitLab/GitCode)

```python
import urllib.request
import json

token = "your_token"
project_id = "owner%2Frepo"
api_base = "https://gitcode.com/api/v4"

# 1. Create Issue
issue_data = {
    "title": "Add feature",
    "description": "## Summary\n\nAdd new feature"
}

req = urllib.request.Request(
    f"{api_base}/projects/{project_id}/issues",
    data=json.dumps(issue_data).encode('utf-8'),
    headers={
        "PRIVATE-TOKEN": token,
        "Content-Type": "application/json"
    }
)

with urllib.request.urlopen(req) as response:
    issue = json.loads(response.read().decode('utf-8'))
    issue_id = issue['iid']
    print(f"Issue created: #{issue_id}")

# 2. Create linked MR
mr_data = {
    "source_branch": "feature-branch",
    "target_branch": "main",
    "title": "Add feature",
    "description": f"## Summary\n\nAdd new feature\n\nFixes #{issue_id}"
}

req = urllib.request.Request(
    f"{api_base}/projects/{project_id}/merge_requests",
    data=json.dumps(mr_data).encode('utf-8'),
    headers={
        "PRIVATE-TOKEN": token,
        "Content-Type": "application/json"
    }
)

with urllib.request.urlopen(req) as response:
    mr = json.loads(response.read().decode('utf-8'))
    print(f"MR created: !{mr['iid']}")
```

## Reference Links

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitLab API Documentation](https://docs.gitlab.com/ee/api/rest/)
- [GitCode Documentation](https://gitcode.com/docs)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)
- [GitLab Personal Access Tokens](https://gitlab.com/-/profile/personal_access_tokens)
