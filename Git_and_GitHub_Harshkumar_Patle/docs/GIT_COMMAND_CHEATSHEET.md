# Git command cheat sheet

```bash
git status
git branch --all
git switch -c branch-name
git add .
git commit -m "Describe the change"
git push -u origin branch-name
git switch main
git merge --no-ff branch-name
git log --oneline --graph --decorate --all
git diff
git diff --staged
git merge --abort
git reset --soft <commit>
git rebase main
git rebase --continue
git rebase --abort
```

## Before every commit
```bash
git status
git diff
git diff --staged
```
Never commit `.env`, credentials, private SSH keys, virtual environments, or generated secrets.
