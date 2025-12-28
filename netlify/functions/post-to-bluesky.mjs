import { schedule } from '@netlify/functions';
import { getStore } from '@netlify/blobs';
import { BskyAgent, RichText } from '@atproto/api';
import { getAllPosts, getPublishablePosts, extractExcerpt, getPostUrl } from './utils/hugo-helpers.js';

/**
 * Main handler for posting new blog posts to Bluesky
 */
const handler = async () => {
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

    // Get the last run timestamp
    const lastRunTimestamp = await store.get('last-run-timestamp', { type: 'text' });
    const lastRunDate = lastRunTimestamp ? new Date(lastRunTimestamp) : null;

    console.log(`Last run: ${lastRunDate ? lastRunDate.toISOString() : 'never (first run)'}`);

    // Get all posts and filter to publishable ones
    const allPosts = await getAllPosts();
    const publishablePosts = getPublishablePosts(allPosts);

    console.log(`Found ${publishablePosts.length} publishable posts`);

    // Filter to only posts published since the last run
    const newPosts = lastRunDate
      ? publishablePosts.filter(post => {
          if (!post.frontMatter.date) return false;
          const postDate = new Date(post.frontMatter.date);
          return postDate > lastRunDate;
        })
      : []; // On first run, don't post anything - just set the timestamp

    console.log(`Found ${newPosts.length} post(s) published since last run`);

    // Update the last run timestamp
    const currentRunTime = new Date().toISOString();
    await store.set('last-run-timestamp', currentRunTime);
    console.log(`Updated last run timestamp to ${currentRunTime}`);

    if (newPosts.length === 0) {
      console.log('No new posts to share on Bluesky');
      return new Response(JSON.stringify({
        message: lastRunDate ? 'No new posts since last run' : 'First run - timestamp set, will check for new posts next time',
        lastRun: lastRunDate ? lastRunDate.toISOString() : null,
        currentRun: currentRunTime,
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    console.log(`Posting ${newPosts.length} new post(s) to Bluesky`);

    const results = [];
    const baseUrl = SITE_URL || 'https://fixthesupremecourt.org';

    // Post each new article to Bluesky
    for (const post of newPosts) {
      try {
        const title = post.frontMatter.title || post.slug;
        const url = getPostUrl(post.slug, baseUrl);

        // Bluesky limit is 300 graphemes (not characters)
        const maxGraphemes = 300;

        // Start with a conservative excerpt length and adjust
        let excerptMaxLength = 100;
        let postText = '';
        let rt = null;

        // Iteratively build the post to fit within grapheme limit
        while (excerptMaxLength >= 0) {
          const excerpt = excerptMaxLength > 0 ? extractExcerpt(post.content, excerptMaxLength) : '';

          // Build post text
          if (excerpt) {
            postText = `${title}\n\n${excerpt}\n\n${url}`;
          } else {
            postText = `${title}\n\n${url}`;
          }

          // Use RichText to count graphemes properly
          rt = new RichText({ text: postText });
          await rt.detectFacets(agent);

          // Check grapheme length
          const graphemeLength = rt.graphemeLength;

          console.log(`Attempt with excerpt length ${excerptMaxLength}: ${graphemeLength}/${maxGraphemes} graphemes`);

          if (graphemeLength <= maxGraphemes) {
            // Found a length that works!
            break;
          }

          // Reduce excerpt length and try again
          excerptMaxLength -= 20;
        }

        if (rt.graphemeLength > maxGraphemes) {
          throw new Error(`Could not fit post within ${maxGraphemes} graphemes (title: ${title.length} chars, URL: ${url.length} chars)`);
        }

        console.log(`Final post: ${rt.graphemeLength}/${maxGraphemes} graphemes`);

        // Post to Bluesky
        const response = await agent.post({
          text: rt.text,
          facets: rt.facets,
          createdAt: new Date().toISOString(),
        });

        console.log(`Successfully posted "${title}" to Bluesky`);

        results.push({
          slug: post.slug,
          title,
          publishDate: post.frontMatter.date,
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

    const successCount = results.filter(r => r.success).length;
    console.log(`Posted ${successCount} of ${newPosts.length} posts to Bluesky`);

    return new Response(JSON.stringify({
      message: `Posted ${successCount} of ${newPosts.length} new posts to Bluesky`,
      lastRun: lastRunDate ? lastRunDate.toISOString() : null,
      currentRun: currentRunTime,
      results,
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    console.error('Error in Bluesky posting function:', error);
    return new Response(JSON.stringify({
      error: error.message,
      stack: error.stack,
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

// Schedule the function to run daily at 9:00 AM UTC
// You can adjust the cron expression as needed
// Current: "0 9 * * *" means 9:00 AM UTC every day
// For 9 AM EST (14:00 UTC): "0 14 * * *"
// For 9 AM PST (17:00 UTC): "0 17 * * *"
export default schedule('0 14 * * *', handler);
