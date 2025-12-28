import { schedule } from '@netlify/functions';
import { getStore } from '@netlify/blobs';
import { BskyAgent, RichText } from '@atproto/api';
import { getAllPosts, getPublishablePosts, extractExcerpt, getPostUrl } from './utils/hugo-helpers.js';

/**
 * Main handler for posting new blog posts to Bluesky
 */
const handler = async (event) => {
  console.log('Starting Bluesky post check...');

  try {
    // Initialize Bluesky agent
    const agent = new BskyAgent({
      service: 'https://bsky.social',
    });

    // Authenticate with Bluesky
    const { BLUESKY_HANDLE, BLUESKY_APP_PASSWORD, SITE_URL } = process.env;

    if (!BLUESKY_HANDLE || !BLUESKY_APP_PASSWORD) {
      throw new Error('Missing BLUESKY_HANDLE or BLUESKY_APP_PASSWORD environment variables');
    }

    await agent.login({
      identifier: BLUESKY_HANDLE,
      password: BLUESKY_APP_PASSWORD,
    });

    console.log('Successfully authenticated with Bluesky');

    // Get Netlify Blobs store for tracking posted articles
    const store = getStore({
      name: 'bluesky-posts',
      consistency: 'strong',
    });

    // Get all posts and filter to publishable ones
    const allPosts = await getAllPosts();
    const publishablePosts = getPublishablePosts(allPosts);

    console.log(`Found ${publishablePosts.length} publishable posts`);

    // Get list of already posted slugs from Netlify Blobs
    const postedSlugsJson = await store.get('posted-slugs', { type: 'json' });
    const postedSlugs = new Set(postedSlugsJson || []);

    console.log(`${postedSlugs.size} posts already posted to Bluesky`);

    // Find new posts that haven't been posted yet
    const newPosts = publishablePosts.filter(post => !postedSlugs.has(post.slug));

    if (newPosts.length === 0) {
      console.log('No new posts to share on Bluesky');
      return {
        statusCode: 200,
        body: JSON.stringify({
          message: 'No new posts to share',
          postedCount: postedSlugs.size,
        }),
      };
    }

    console.log(`Found ${newPosts.length} new post(s) to share on Bluesky`);

    const results = [];
    const baseUrl = SITE_URL || 'https://fixthesupremecourt.org';

    // Post each new article to Bluesky
    for (const post of newPosts) {
      try {
        const title = post.frontMatter.title || post.slug;
        const excerpt = extractExcerpt(post.content, 200); // Leave room for title and URL
        const url = getPostUrl(post.slug, baseUrl);

        // Create the Bluesky post text
        // Format: Title\n\nExcerpt\n\nURL
        const postText = `${title}\n\n${excerpt}\n\n${url}`;

        // Use RichText to properly handle facets (links, mentions, etc.)
        const rt = new RichText({ text: postText });
        await rt.detectFacets(agent);

        // Post to Bluesky
        const response = await agent.post({
          text: rt.text,
          facets: rt.facets,
          createdAt: new Date().toISOString(),
        });

        console.log(`Successfully posted "${title}" to Bluesky`);

        // Add to posted slugs
        postedSlugs.add(post.slug);

        results.push({
          slug: post.slug,
          title,
          success: true,
          uri: response.uri,
        });
      } catch (error) {
        console.error(`Error posting "${post.slug}":`, error);
        results.push({
          slug: post.slug,
          title: post.frontMatter.title,
          success: false,
          error: error.message,
        });
      }
    }

    // Update the posted slugs in Netlify Blobs
    await store.setJSON('posted-slugs', Array.from(postedSlugs));

    console.log('Updated posted slugs in Netlify Blobs');

    return {
      statusCode: 200,
      body: JSON.stringify({
        message: `Posted ${results.filter(r => r.success).length} of ${newPosts.length} new posts to Bluesky`,
        results,
        totalPosted: postedSlugs.size,
      }),
    };
  } catch (error) {
    console.error('Error in Bluesky posting function:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: error.message,
        stack: error.stack,
      }),
    };
  }
};

// Schedule the function to run daily at 9:00 AM UTC
// You can adjust the cron expression as needed
// Current: "0 9 * * *" means 9:00 AM UTC every day
// For 9 AM EST (14:00 UTC): "0 14 * * *"
// For 9 AM PST (17:00 UTC): "0 17 * * *"
export default schedule('0 14 * * *', handler);
