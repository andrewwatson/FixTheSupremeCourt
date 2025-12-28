# Netlify Functions - Bluesky Auto-Posting

This directory contains Netlify Functions that automatically post new Hugo blog posts to Bluesky.

## Overview

The `post-to-bluesky.mjs` scheduled function runs daily at 9:00 AM EST to:
1. Scan all Hugo posts in `content/posts/`
2. Filter out drafts and future-dated posts
3. Check Netlify Blobs to see which posts have already been posted to Bluesky
4. Post new articles to Bluesky with title, excerpt, and URL
5. Track posted articles in Netlify Blobs

## Setup

### 1. Install Dependencies

```bash
npm install
```

This installs:
- `@netlify/functions` - Netlify Functions runtime
- `@netlify/blobs` - Netlify Blobs for tracking posted articles
- `@atproto/api` - Bluesky API client
- `gray-matter` - Parse Hugo front matter

### 2. Set Environment Variables

In your Netlify site settings, add the following environment variables:

- **`BLUESKY_HANDLE`** (required) - Your Bluesky handle (e.g., `yourusername.bsky.social`)
- **`BLUESKY_APP_PASSWORD`** (required) - A Bluesky app password (NOT your main password)
- **`SITE_URL`** (optional) - Your site's base URL (defaults to `https://fixthesupremecourt.org`)

#### Creating a Bluesky App Password

1. Log in to Bluesky at https://bsky.app
2. Go to Settings → Privacy and Security → App Passwords
3. Click "Add App Password"
4. Give it a name (e.g., "Netlify Auto-Posting")
5. Copy the generated password
6. Add it to Netlify as `BLUESKY_APP_PASSWORD`

**Important:** Use an app password, not your main account password. This is more secure and can be revoked independently.

### 3. Deploy to Netlify

The function will automatically deploy when you push to your repository. The scheduled function will start running daily at 9:00 AM EST.

## Schedule Configuration

The function is currently set to run at **9:00 AM EST (14:00 UTC)** daily.

To change the schedule, edit the cron expression in `post-to-bluesky.mjs`:

```javascript
export default schedule('0 14 * * *', handler);
```

Common cron expressions:
- `0 14 * * *` - 9:00 AM EST / 2:00 PM UTC (current)
- `0 17 * * *` - 9:00 AM PST / 5:00 PM UTC
- `0 13 * * *` - 9:00 AM EDT / 1:00 PM UTC (daylight saving time)
- `0 */6 * * *` - Every 6 hours
- `0 9,17 * * *` - 9:00 AM and 5:00 PM UTC

## Post Format

Posts to Bluesky follow this format:

```
[Post Title]

[Excerpt from post content - up to 200 characters]

[Full URL to post]
```

The excerpt is automatically extracted from:
1. Content before the `<!--more-->` marker (if present)
2. The beginning of the post content

Markdown formatting is stripped, and text is truncated to fit within Bluesky's character limits.

## Tracking Posted Articles

The function uses Netlify Blobs to track which posts have been shared:

- **Store name:** `bluesky-posts`
- **Key:** `posted-slugs`
- **Format:** JSON array of post slugs

You can view or manually edit this data using the Netlify CLI:

```bash
# View posted slugs
netlify blobs:get bluesky-posts posted-slugs

# Manually add a slug (if you want to skip posting something)
netlify blobs:set bluesky-posts posted-slugs '["slug-1", "slug-2", "slug-3"]'

# Clear all tracking (will repost everything)
netlify blobs:delete bluesky-posts posted-slugs
```

## Testing Locally

You can test the function locally using the Netlify CLI:

```bash
# Install Netlify CLI if you haven't already
npm install -g netlify-cli

# Set environment variables in a .env file (don't commit this!)
echo 'BLUESKY_HANDLE=your.handle.bsky.social' > .env
echo 'BLUESKY_APP_PASSWORD=your-app-password' >> .env

# Run the function locally
netlify functions:invoke post-to-bluesky
```

## Manual Triggering

You can also manually trigger the function through the Netlify UI:

1. Go to your Netlify site dashboard
2. Navigate to Functions
3. Find `post-to-bluesky`
4. Click "Trigger function"

## Troubleshooting

### "No new posts to share"

This is normal if:
- All publishable posts have already been posted
- All posts are marked as drafts
- All posts have future publish dates

### "Missing BLUESKY_HANDLE or BLUESKY_APP_PASSWORD"

Check that environment variables are set correctly in Netlify site settings.

### "Authentication failed"

- Verify your app password is correct
- Make sure you're using an app password, not your main password
- Check that your handle includes the full domain (e.g., `username.bsky.social`)

### Posts not appearing on Bluesky

- Check the function logs in Netlify dashboard
- Verify the post isn't a draft (`draft: false` in front matter)
- Verify the post date isn't in the future

## File Structure

```
netlify/
└── functions/
    ├── README.md                    # This file
    ├── post-to-bluesky.mjs         # Main scheduled function
    └── utils/
        └── hugo-helpers.js         # Helper utilities for parsing Hugo posts
```

## How It Works

1. **Scheduled Execution**: Netlify's scheduler triggers the function daily at 9 AM EST
2. **Authentication**: Function authenticates with Bluesky using app password
3. **Fetch Posts**: Reads all markdown files from `content/posts/`
4. **Filter**: Removes drafts and future-dated posts
5. **Check Tracking**: Queries Netlify Blobs to see which posts were already shared
6. **Post New Content**: For each new post:
   - Extracts title and excerpt
   - Generates post URL
   - Posts to Bluesky with proper link detection
   - Updates tracking in Netlify Blobs
7. **Return Results**: Returns summary of what was posted

## Future Enhancements

Possible improvements:
- Add hashtags based on post categories/tags
- Support for posting images/cards
- Retry logic for failed posts
- Notification on successful/failed posts
- Support for multiple social platforms
