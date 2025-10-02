/**
 * Cloudflare Worker for Voither Landing Page
 * Handles static site hosting with environment variable injection
 */

export interface Env {
  GEMINI_API_KEY: string;
  ASSETS: Fetcher;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Handle CORS for API requests
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    // API endpoint for Gemini API key (for client-side access)
    if (url.pathname === '/api/config') {
      return new Response(
        JSON.stringify({
          GEMINI_API_KEY: env.GEMINI_API_KEY,
        }),
        {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        }
      );
    }

    // Handle static assets
    try {
      // Get the asset from the Workers Sites asset store
      const response = await env.ASSETS.fetch(request);

      // For HTML files, inject environment variables
      if (response.headers.get('Content-Type')?.includes('text/html')) {
        const html = await response.text();

        // Replace environment variable placeholders
        const modifiedHtml = html.replace(
          /process\.env\.GEMINI_API_KEY/g,
          `"${env.GEMINI_API_KEY}"`
        );

        return new Response(modifiedHtml, {
          status: response.status,
          statusText: response.statusText,
          headers: {
            ...response.headers,
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

      // Return other assets as-is with CORS headers
      const modifiedResponse = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: {
          ...response.headers,
          'Access-Control-Allow-Origin': '*',
        },
      });

      return modifiedResponse;
    } catch (error) {
      return new Response('Asset not found', { status: 404 });
    }
  },
};