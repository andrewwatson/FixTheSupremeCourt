import { readdir, readFile } from 'fs/promises';
import { join } from 'path';
import matter from 'gray-matter';

/**
 * Get all Hugo blog posts from the content/posts directory
 * @returns {Promise<Array>} Array of post objects with metadata and content
 */
export async function getAllPosts() {
  const postsDirectory = join(process.cwd(), 'content', 'posts');

  try {
    const files = await readdir(postsDirectory);
    const markdownFiles = files.filter(file => file.endsWith('.md'));

    const posts = await Promise.all(
      markdownFiles.map(async (filename) => {
        const filePath = join(postsDirectory, filename);
        const fileContents = await readFile(filePath, 'utf8');
        const { data, content } = matter(fileContents);

        // Extract slug from filename (remove .md extension)
        const slug = filename.replace(/\.md$/, '');

        return {
          slug,
          filename,
          frontMatter: data,
          content,
        };
      })
    );

    return posts;
  } catch (error) {
    console.error('Error reading posts:', error);
    throw error;
  }
}

/**
 * Filter out draft posts and future-dated posts
 * @param {Array} posts - Array of post objects
 * @returns {Array} Filtered posts that should be published
 */
export function getPublishablePosts(posts) {
  const now = new Date();

  return posts.filter(post => {
    // Skip drafts
    if (post.frontMatter.draft === true) {
      return false;
    }

    // Skip future-dated posts
    if (post.frontMatter.date) {
      const postDate = new Date(post.frontMatter.date);
      if (postDate > now) {
        return false;
      }
    }

    return true;
  });
}

/**
 * Extract an excerpt from post content
 * @param {string} content - Post content
 * @param {number} maxLength - Maximum length of excerpt
 * @returns {string} Excerpt text
 */
export function extractExcerpt(content, maxLength = 280) {
  // First, try to get content before <!--more--> marker
  const moreMarkerIndex = content.indexOf('<!--more-->');
  let excerpt = moreMarkerIndex > -1
    ? content.substring(0, moreMarkerIndex).trim()
    : content;

  // Remove markdown headers
  excerpt = excerpt.replace(/^#{1,6}\s+/gm, '');

  // Remove markdown links but keep text
  excerpt = excerpt.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

  // Remove markdown bold/italic
  excerpt = excerpt.replace(/[*_]{1,2}([^*_]+)[*_]{1,2}/g, '$1');

  // Remove extra whitespace and newlines
  excerpt = excerpt.replace(/\s+/g, ' ').trim();

  // Truncate if too long
  if (excerpt.length > maxLength) {
    excerpt = excerpt.substring(0, maxLength - 3).trim() + '...';
  }

  return excerpt;
}

/**
 * Generate the full URL for a post
 * @param {string} slug - Post slug
 * @param {string} baseUrl - Base URL of the site
 * @returns {string} Full post URL
 */
export function getPostUrl(slug, baseUrl = 'https://fixthesupremecourt.org') {
  // Remove trailing slash from baseUrl if present
  const cleanBaseUrl = baseUrl.replace(/\/$/, '');
  return `${cleanBaseUrl}/posts/${slug}/`;
}
