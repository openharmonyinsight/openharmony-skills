# Extended oh-gc Commands

Use this reference for less common GitCode operations. For everyday Issue and PR work, prefer `common-issue-pr-commands.md`.

## Releases

```bash
oh-gc release create
oh-gc release create v1.0.0
oh-gc release create --prerelease
oh-gc release create v1.0.0 --notes "..."
```

## Repo Configuration

```bash
oh-gc repo list
oh-gc repo list --org myorg
oh-gc repo create myrepo
oh-gc repo create myrepo --org myorg
oh-gc repo delete --yes
oh-gc repo fork
oh-gc repo fork --org myorg
oh-gc repo forks
oh-gc repo settings
oh-gc repo settings --disable-fork
oh-gc repo languages
oh-gc repo contributors
oh-gc repo contributors --stats
oh-gc repo events
oh-gc repo events --filter push
oh-gc repo stats --branch main
oh-gc repo stats --downloads
oh-gc repo archive --password secret
oh-gc repo archive --open --password secret
oh-gc repo transition
oh-gc repo transition --mode 2
oh-gc repo module --wiki --issues
oh-gc repo module --no-fork
oh-gc repo roles
oh-gc repo list --user alice
oh-gc repo list --visibility private
oh-gc repo get-remote
oh-gc repo set-remote upstream
oh-gc repo view
oh-gc repo update --description "..."
oh-gc repo transfer <new-owner>
```

Remote override storage: `.gitcode/oh-gc-config.json`.

## Search

```bash
oh-gc search repos "keyword"
oh-gc search issues "keyword"
oh-gc search code "keyword"
```

## User

```bash
oh-gc user view
oh-gc user view alice
oh-gc user edit --name "New Name" --bio "..."
oh-gc user edit --avatar "https://..."
oh-gc user emails
oh-gc user followers
oh-gc user following
oh-gc user events alice
oh-gc user events alice --year 2024
oh-gc user search alice
oh-gc user search bob --sort joined_at
oh-gc user namespace alice
oh-gc user namespaces
oh-gc user namespaces --mode project
oh-gc user keys
oh-gc user key-add --title "My Key" --key "ssh-rsa ..."
oh-gc user key-delete 123
oh-gc user starred
oh-gc user starred alice
oh-gc user subscriptions
oh-gc user subscriptions alice
# Basic issue queries
oh-gc user issues
oh-gc user issues --state closed --filter created
oh-gc user issues --state open --filter assigned

# Pagination: default per-page=20, max 100
oh-gc user issues --per-page 100
oh-gc user issues --per-page 50 --page 2

# Time filters
# --since: 按更新时间过滤（ISO 8601）
oh-gc user issues --since "2024-01-01T00:00:00Z"

# --created-at: 按创建时间范围过滤，格式为 START..END（两端必填）
oh-gc user issues --created-at "2024-01-01..2025-12-31"

# --finished-at: 按完成时间范围过滤
oh-gc user issues --state closed --finished-at "2025-01-01..2025-12-31"

# Other filters
oh-gc user issues --labels "bug,P0"
oh-gc user issues --sort updated_at --direction asc
oh-gc user prs
oh-gc user prs --state merged --scope assigned_to_me
oh-gc user prs --source-branch feature --target-branch main
oh-gc user orgs alice
oh-gc user membership myorg
oh-gc user leave-org myorg
```

## Branches

```bash
oh-gc branch list
oh-gc branch list --protected
oh-gc branch get <name>
oh-gc branch create <name> --ref <sha/branch>
oh-gc branch delete <name>
oh-gc branch protect <name>
oh-gc branch protect <name> --enforce-admins
oh-gc branch protect <name> --require-status-checks ci,lint
oh-gc branch protect <name> --dismiss-stale-reviews
oh-gc branch protect <name> --unprotect
oh-gc branch protect-rules
oh-gc branch protect-rule-create <pattern> --pusher <roles> --merger <roles>
oh-gc branch protect-rule-update <pattern> --pusher <roles> --merger <roles>
oh-gc branch protect-rule-delete <pattern>
```

## Commits

```bash
oh-gc commit list
oh-gc commit list --sha main
oh-gc commit get <sha>
oh-gc commit diff <sha>
oh-gc commit compare <base> <head>
oh-gc commit comments <sha>
oh-gc commit comment <sha> --body "text"
```

## Files

```bash
oh-gc file get <path>
oh-gc file raw <path> --ref main
oh-gc file list
oh-gc file create <path> --content "text" --message "msg"
oh-gc file update <path> --sha <sha> --content "text" --message "msg"
oh-gc file delete <path> --sha <sha> --message "msg"
```

## Collaborators

```bash
oh-gc collaborator list
oh-gc collaborator add <username>
oh-gc collaborator remove <username>
oh-gc collaborator permission <username>
```

## Labels

```bash
oh-gc label list
oh-gc label create
oh-gc label update <name>
oh-gc label delete <name>
```

## Milestones

```bash
oh-gc milestone list
oh-gc milestone get <number>
oh-gc milestone create
oh-gc milestone update <number>
oh-gc milestone delete <number>
```

## Webhooks

```bash
oh-gc hook list
oh-gc hook get <id>
oh-gc hook create
oh-gc hook delete <id>
```

## Tags

```bash
oh-gc tag list
oh-gc tag create <name> --ref <sha/branch>
oh-gc tag delete <name>
oh-gc tag protect <name>
oh-gc tag protect-get <name>
oh-gc tag protect-create <name> --access-level 40
oh-gc tag protect-update <name> --access-level 30
oh-gc tag protect-delete <name>
```

## Organizations

```bash
oh-gc org list
oh-gc org view <org>
oh-gc org members <org>
```
