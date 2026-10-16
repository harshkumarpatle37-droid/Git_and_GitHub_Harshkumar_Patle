# Git & GitHub DevOps Assignment Report

**Student name:** Harshkumar Patle  
**Operating system:** Linux  
**Project:** Flask To-Do application  
**GitHub repository:`https://github.com/harshkumarpatle37-droid/Git_and_GitHub_Harshkumar_Patle`

> Replace the repository placeholder with your real GitHub URL. Insert your own screenshots in `docs/screenshots/` and link them in this report. Do not claim a screenshot was captured unless you have captured it.

## Objective
Practise a complete Git workflow using a Flask project: SSH setup, branch creation, merge, JSON changes, conflict resolution, parallel feature development, sequential commits, `git reset --soft`, and rebase while preserving individual commits.

## Environment setup
```bash
git --version
python3 --version
ssh -V
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`. Check `http://127.0.0.1:5000/api` and `http://127.0.0.1:5000/items`.

## Task 1 — Repository setup and first branch

### 1. Create a GitHub repository
Create a public repository named `Git_and_GitHub_Harshkumar_Patle`. Add a README only if you intend to clone that initialized repository; otherwise create an empty repository.

### 2. Configure SSH on Linux
```bash
ssh-keygen -t ed25519 -C "your-github-email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```
Copy the public key output (never share `id_ed25519`, the private key). In GitHub, open **Settings → SSH and GPG keys → New SSH key**, paste the public key, and save it.
```bash
ssh -T git@github.com
```
The first connection may ask you to confirm GitHub's host fingerprint. Verify it against GitHub's published SSH key fingerprints before accepting.

### 3. Clone the repository
Replace the URL with the SSH URL shown on your GitHub repository:
```bash
git clone git@github.com:YOUR_USERNAME/Git_and_GitHub_Harshkumar_Patle.git
cd Git_and_GitHub_Harshkumar_Patle
git config user.name "Harshkumar Patle"
git config user.email "your-github-email@example.com"
```
Copy the provided project files into this cloned directory if the repository was created empty. If you are using the ZIP as your project source, copy its contents into the cloned repository, but do not nest a second copy of the project folder inside it.

### 4. Create your username branch and merge it
```bash
git switch -c YOUR_USERNAME
git add app.py templates static requirements.txt .env.example .gitignore README.md data
git commit -m "Add Flask To-Do application"
git push -u origin YOUR_USERNAME
git switch main
git pull origin main
git merge --no-ff YOUR_USERNAME -m "Merge initial Flask project"
git push origin main
```
If the default branch is called `master`, use `master` in place of `main`. If Git reports unrelated histories because both sides independently have commits, stop and inspect the repository history rather than blindly forcing a merge.

**Evidence to capture:** repository page, SSH success, branch list, commit output, merge output, and pushed main branch.

## Task 2 — Update JSON and resolve conflicts

This task deliberately creates a conflict in `api_config.json`.

```bash
git switch main
git pull origin main
git switch -c YOUR_USERNAME_new
```
The project includes `api_config.json`, which is read by `GET /api`. On branch `YOUR_USERNAME_new`, update its version to `"1.1"` and keep the owner as `"YOUR_USERNAME"`:
```json
{
  "name": "To-Do API",
  "version": "1.1",
  "routes": ["/api", "/submittodoitem", "/items"],
  "owner": "YOUR_USERNAME"
}
```
```bash
git add api_config.json
git commit -m "Add API configuration JSON"
git push -u origin YOUR_USERNAME_new
```
Now create a conflicting change on main:
```bash
git switch main
```
Edit the same `api_config.json` lines on `main` so `version` is `"1.0-main"` and `owner` is `"main-branch"`, then:
```bash
git add api_config.json
git commit -m "Update API config on main"
git push origin main
```
Merge the new branch:
```bash
git merge YOUR_USERNAME_new
```
Git should report a conflict in `api_config.json`. To accept the changes from the `_new` branch as the assignment specifies:
```bash
git checkout --theirs api_config.json
```
In this merge, `--theirs` refers to the branch being merged (`YOUR_USERNAME_new`). Inspect the result, then:
```bash
cat api_config.json
git add api_config.json
git commit -m "Resolve API config conflict using new branch"
git push origin main
```
If Git does not produce a conflict, confirm that the two branches changed the same lines and repeat the controlled conflict setup. Do not run `git checkout --theirs` outside the intended merge.

**Evidence to capture:** both branch versions, conflict markers/status, resolved JSON, resolution commit, and remote push.

## Task 3 — Parallel feature development

Create two branches from the current main:
```bash
git switch main
git pull origin main
git switch -c master_1
```

### Branch `master_1`: frontend To-Do form
The provided project already contains a To-Do form with `Item Name` and `Item Description`. Stage and commit this feature on `master_1` (if these files were introduced in Task 1, make a small meaningful enhancement such as a clear validation message and commit that enhancement):
```bash
git add templates/index.html static/app.js static/style.css
git commit -m "Build To-Do form frontend"
```
Add fields for Item ID, Item UUID, and Item Hash in the next task, not yet.

### Branch `master_2`: backend API and MongoDB
```bash
git switch main
git switch -c master_2
```
The provided Flask app already implements `POST /submittodoitem`, accepts `itemName` and `itemDescription`, and stores them in MongoDB when `MONGO_URI` is configured. It falls back to local JSON storage when MongoDB is not configured or unavailable.
```bash
git add app.py requirements.txt .env.example
git commit -m "Add To-Do submission API and storage"
```
Merge both feature branches into main:
```bash
git switch main
git merge --no-ff master_1 -m "Merge To-Do frontend"
git merge --no-ff master_2 -m "Merge To-Do backend API"
git push origin main
```
If Git reports “already up to date” because the initial files were committed earlier, make and commit a distinct, meaningful change on the relevant feature branch before merging. The important evidence is that both branches contain separate feature commits and both are merged into main.

### API test
Start the app and, in another terminal, run:
```bash
curl http://127.0.0.1:5000/api
curl -X POST http://127.0.0.1:5000/submittodoitem \
  -H 'Content-Type: application/json' \
  -d '{"itemName":"Git practice","itemDescription":"Practice branches and merges"}'
curl http://127.0.0.1:5000/items
```
Without a configured MongoDB URI, successful submissions are stored in `data/items.json`.

## Task 4 — Sequential commits, reset and rebase

### 1. Create / switch to `master_1`
```bash
git switch main
git pull origin main
git switch master_1
```
Edit `templates/index.html` to add form fields for Item ID, Item UUID, and Item Hash. For this exercise, keep the form fields as disabled/read-only display fields because the backend generates these values. Add them one at a time and commit each separately. For a genuine sequential history, edit and commit Item ID first, then UUID, then Hash:
```bash
git add templates/index.html
git commit -m "Add Item ID field"
# Edit the file to add Item UUID, then:
git add templates/index.html
git commit -m "Add Item UUID field"
# Edit the file to add Item Hash, then:
git add templates/index.html
git commit -m "Add Item Hash field"
```
Update the frontend JavaScript to populate those read-only fields from the response as needed and commit the change separately if desired. Keep each requested field commit separate; do not squash them.

### 2. Merge into main
```bash
git switch main
git merge --no-ff master_1 -m "Merge item metadata fields"
git push origin main
```

### 3. Demonstrate `git reset --soft`
Create a safety branch first:
```bash
git branch backup-before-soft-reset
git log --oneline --decorate -8
```
Find the commit whose message is `Add Item ID field` and copy its hash. To reset the current `main` branch to that commit while keeping later changes staged:
```bash
git reset --soft <ITEM_ID_COMMIT_HASH>
git status
```
This intentionally moves `main` backwards locally and stages the later changes. **Do not force-push this history rewrite to a shared repository.** Re-commit the staged state as instructed:
```bash
git commit -m "Recommit item metadata changes after soft reset"
```
Then merge the updated state into main only if your working branch is different. If you reset main itself, it is already main. Push normally only if the resulting history is a fast-forward; otherwise use a new branch and open a pull request, or coordinate with your mentor before rewriting shared history. To preserve a clean remote history, you can perform the demonstration on a separate local practice branch instead.

### 4. Demonstrate rebase without squashing
Use the backup branch to protect the original commits. First update main, then rebase the feature branch:
```bash
git switch main
git pull origin main
git switch master_1
git rebase main
```
Resolve any conflicts by editing the files, removing conflict markers, then:
```bash
git add <resolved-file>
git rebase --continue
```
Repeat if further conflicts appear. Use `git rebase --abort` to return to the pre-rebase state if needed. Verify the three separate field commits remain:
```bash
git log --oneline --graph --decorate --all
```
Push the rebased branch only if it has not already been pushed; if it was pushed before rebase, coordinate before using `git push --force-with-lease`. Never use plain `git push --force` on a shared branch.

**Important:** Because Task 4 asks to reset and rebase the same history, run these operations in a practice branch and keep `backup-before-soft-reset` until the mentor verifies the evidence. Do not force-push rewritten history to `main`.

## Screenshot checklist
Save screenshots as PNG files in `docs/screenshots/` and update the checklist below:
- [ ] `01-github-repository.png` — repository created.
- [ ] `02-ssh-authentication.png` — `ssh -T git@github.com`.
- [ ] `03-first-branch-commit.png` — branch and commit.
- [ ] `04-merge-first-branch.png` — merge into main.
- [ ] `05-json-conflict.png` — merge conflict status.
- [ ] `06-conflict-resolved.png` — resolved JSON and commit.
- [ ] `07-master-1-frontend.png` — frontend feature branch and commit.
- [ ] `08-master-2-api.png` — backend feature branch and commit.
- [ ] `09-feature-merges.png` — both feature merges.
- [ ] `10-api-test.png` — curl requests and successful output.
- [ ] `11-sequential-commits.png` — three separate field commits.
- [ ] `12-soft-reset.png` — `git status` after `git reset --soft`.
- [ ] `13-rebase-history.png` — `git log --graph` proving separate commits.

## Conclusion
This project and workflow demonstrate SSH authentication, repository setup, feature branching, merge conflict resolution, Flask API development, JSON/MongoDB storage, sequential commits, soft reset, and rebase. Complete the commands on your own GitHub repository and attach authentic screenshots before submission.
