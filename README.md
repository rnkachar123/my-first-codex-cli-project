# my-first-codex-cli-project

## Git sync helper

If you are working in an environment where `origin` is not configured, use the safe pull helper instead of running `git fetch origin main` directly.

```bash
./scripts/safe_pull_main.sh
```

Behavior:
- If `origin` exists, it fetches `main` and runs `git pull --rebase origin main`.
- If `origin` is missing, it exits cleanly with instructions to add the remote.

## Configure `origin` when missing

If `./scripts/safe_pull_main.sh` says your `origin` remote is missing, run:

```bash
git remote add origin https://github.com/<your-username>/my-first-codex-cli-project.git
```

Alternative SSH format:

```bash
git remote add origin git@github.com:<your-username>/my-first-codex-cli-project.git
```

Verify configuration:

```bash
git remote -v
```

Then sync:

```bash
./scripts/safe_pull_main.sh
```

If a remote named `origin` already exists but points to the wrong URL, update it with:

```bash
git remote set-url origin https://github.com/<your-username>/my-first-codex-cli-project.git
```
