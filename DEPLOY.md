# Deploying to GitHub Pages

This guide walks through deploying your personal website to GitHub Pages with your custom domain (ericaskelson.com).

## Prerequisites

- GitHub account (you have this)
- Domain registered (ericaskelson.com via Squarespace)
- Git repository initialized (done)

---

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `personal-website` (or `ericaskelson.com` - either works)
3. **Important:** Set to **Private** if you want to test before going public
4. Don't initialize with README (we already have files)
5. Click "Create repository"

---

## Step 2: Push Your Code

After creating the repo, GitHub will show commands. Run these in your project folder:

```bash
git remote add origin https://github.com/YOUR_USERNAME/personal-website.git
git branch -M main
git push -u origin main
```

---

## Step 3: Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** (tab at the top)
3. Scroll down to **Pages** (left sidebar)
4. Under "Source", select:
   - **Branch:** `main`
   - **Folder:** `/ (root)`
5. Click **Save**

Your site will be live at `https://YOUR_USERNAME.github.io/personal-website/` within a few minutes.

---

## Step 4: Configure Custom Domain (ericaskelson.com)

### On GitHub:

1. In the Pages settings, under "Custom domain"
2. Enter: `ericaskelson.com`
3. Click **Save**
4. Check "Enforce HTTPS" (after DNS propagates)

### On Squarespace (DNS Settings):

1. Log into Squarespace
2. Go to **Domains** → **ericaskelson.com** → **DNS Settings**
3. Add these records:

**For apex domain (ericaskelson.com):**

| Type | Host | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

**For www subdomain (optional but recommended):**

| Type | Host | Value |
|------|------|-------|
| CNAME | www | YOUR_USERNAME.github.io |

4. Save changes
5. Wait for DNS propagation (can take up to 48 hours, usually faster)

---

## Step 5: Create CNAME File

GitHub needs a CNAME file in your repo. Create it:

```
ericaskelson.com
```

This file should already exist if you configured the custom domain in GitHub's UI, but you can also create it manually.

---

## Step 6: Verify Deployment

1. Wait a few minutes after pushing
2. Visit `https://ericaskelson.com`
3. Check that HTTPS works (padlock icon)
4. Test all pages: Home, Resume, Blog

---

## Updating Your Site

After the initial setup, updating is simple:

```bash
git add -A
git commit -m "Your changes"
git push
```

GitHub Pages will automatically rebuild within a few minutes.

---

## Troubleshooting

### "404 - File not found"
- Make sure `index.html` is in the root directory
- Check that GitHub Pages source is set to the correct branch

### DNS not working
- Verify DNS records are correct in Squarespace
- Use https://dnschecker.org to verify propagation
- Wait up to 48 hours for full propagation

### HTTPS not available
- DNS must fully propagate first
- Go to repo Settings → Pages → Re-check "Enforce HTTPS"

### Changes not appearing
- Hard refresh: Ctrl+Shift+R
- GitHub Pages can take 2-10 minutes to rebuild
- Check the "Actions" tab for build status

---

## Private Testing

If you want to keep it private while testing:

1. Keep the repo private
2. You can still access it at `https://YOUR_USERNAME.github.io/personal-website/`
3. Only you (logged into GitHub) can see it
4. When ready, make the repo public

Note: Custom domains require the repo to be public on the free GitHub plan. For private repos with custom domains, you need GitHub Pro.

---

## Quick Reference

| What | Where |
|------|-------|
| GitHub repo settings | `https://github.com/USERNAME/REPO/settings` |
| GitHub Pages settings | `https://github.com/USERNAME/REPO/settings/pages` |
| Squarespace DNS | Domains → ericaskelson.com → DNS Settings |
| Check DNS propagation | https://dnschecker.org |
| GitHub Pages IPs | 185.199.108-111.153 |
