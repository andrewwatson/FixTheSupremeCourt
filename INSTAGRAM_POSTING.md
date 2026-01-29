# Instagram Posting Guide

## Quick Start

To prepare an Instagram post for any blog article:

```bash
./instagram_post.sh --post POST-SLUG
```

For example:
```bash
./instagram_post.sh --post ieepa-tariff-delay
./instagram_post.sh --post judicial-conflicts-comparison
```

## What It Does

The script automatically:

1. ✅ **Finds your blog post** by slug (filename without .md)
2. ✅ **Generates Instagram image** (1080x1080) if needed
3. ✅ **Creates formatted caption** with:
   - Post title
   - Link to full article
   - Relevant hashtags based on post tags
4. ✅ **Copies caption to clipboard** - ready to paste!
5. ✅ **Shows you which image to upload**

## Options

```bash
# Basic usage
./instagram_post.sh --post POST-SLUG

# Auto-open Instagram in browser
./instagram_post.sh --post POST-SLUG --open
```

## Posting to Instagram

After running the script:

### On Desktop (instagram.com)
1. Go to https://www.instagram.com (or use `--open` flag)
2. Click the **+** button (Create)
3. Select **Post**
4. Upload the image shown in the script output
5. Paste the caption (already in your clipboard - just Cmd+V)
6. Click **Share**

### On Mobile
1. Open Instagram app
2. Tap the **+** button
3. Select **Post**
4. Choose the image (you'll need to transfer it to your phone via AirDrop or iCloud)
5. Paste the caption
6. Share

## Hashtag Strategy

The script automatically selects hashtags based on your post's tags:

| Post Tags | Hashtags Included |
|-----------|-------------------|
| `corruption`, `ethics` | #SupremeCourt #SCOTUS #JudicialEthics #Corruption #Transparency |
| `executive power` | #ExecutivePower #Constitution #ChecksAndBalances #RuleOfLaw |
| `shadow docket` | #ShadowDocket #Transparency #EmergencyDocket |
| `partisanship` | #PartisanCourt #CourtReform #Accountability |
| `reform` | #CourtReform #TermLimits #ExpandTheCourt |

The script uses max 10 hashtags (Instagram's recommended limit).

## Example Output

```
📝 Post: The Supreme Court's Ominous Silence on Trump's Tariff Powers
🏷️  Tags: executive power, corruption, partisanship
🖼️  Image: static/thumbnails/ieepa-tariff-delay_modern.png

✅ Caption copied to clipboard!

============================================================
📱 INSTAGRAM POSTING INSTRUCTIONS
============================================================

1. Upload this image:
   /Users/andy/development/projects/FixTheSupremeCourt/static/thumbnails/ieepa-tariff-delay_modern.png

2. Paste the caption (already in your clipboard)

3. Post!
```

## Caption Format

The generated caption follows this format:

```
[Post Title]

Read the full article: https://fixthesupremecourt.org/posts/[slug]/

Why Supreme Court reform matters 👇

#SupremeCourt #SCOTUS #ExecutivePower #Constitution
#ChecksAndBalances #Democracy #RuleOfLaw

#LinkInBio #FixTheCourt
```

## Full Automation (Advanced)

For true automation, you'd need:

1. **Instagram Business Account**
2. **Facebook Developer App** with Instagram Graph API access
3. **Access tokens** and authentication setup

This requires:
- Converting to Business/Creator account
- Linking to Facebook Page
- Getting app approved by Meta
- Setting up OAuth tokens

If you want to explore this, I can help set it up, but the semi-automated approach above is usually faster for posting individual articles.

## Troubleshooting

### "Post not found"
- Make sure you're using the post slug (filename without .md extension)
- Check that the post exists in `content/posts/`

### "Instagram image not found"
- The script will auto-generate it
- If generation fails, run manually: `python generate_thumbnails_pro.py --post POST-SLUG`

### "Caption not copied"
- Clipboard copy requires macOS `pbcopy` command
- If it fails, the caption will be printed to terminal instead - just copy manually

## Batch Posting

To prepare multiple posts at once:

```bash
for post in ieepa-tariff-delay judicial-conflicts-comparison; do
    ./instagram_post.sh --post $post
    echo "Press Enter for next post..."
    read
done
```

This will prepare each post one at a time, pausing between them.
