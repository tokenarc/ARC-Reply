/**
 * ARC Reply - Cloudflare Workers Webhook Handler
 * Handles Telegram bot webhook updates and routes to bot logic
 */

import { Telegraf } from 'telegraf';

// Initialize bot with Telegram token
const bot = new Telegraf(env.TELEGRAM_BOT_TOKEN);

/**
 * Handle webhook POST requests from Telegram
 */
async function handleWebhook(request, env, ctx) {
  // Only accept POST requests
  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    // Parse incoming JSON from Telegram
    const update = await request.json();

    // Log incoming update
    console.log('Incoming update:', JSON.stringify(update, null, 2));

    // Process update through bot middleware
    await bot.handleUpdate(update);

    // Return success response
    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Webhook error:', error);
    return new Response(JSON.stringify({ ok: false, error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

/**
 * Handle health check requests
 */
async function handleHealthCheck(request) {
  if (request.url.endsWith('/health')) {
    return new Response(JSON.stringify({ status: 'healthy' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }
  return null;
}

/**
 * Main fetch handler for Cloudflare Workers
 */
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Health check endpoint
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ status: 'healthy', bot: 'ARC Reply' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Webhook endpoint for Telegram updates
    if (url.pathname === '/webhook' && request.method === 'POST') {
      return handleWebhook(request, env, ctx);
    }

    // Root endpoint
    if (url.pathname === '/') {
      return new Response(JSON.stringify({ 
        message: 'ARC Reply Bot - Cloudflare Workers',
        version: '1.0.0',
        endpoints: {
          webhook: '/webhook (POST)',
          health: '/health (GET)',
        }
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // 404 for unknown routes
    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' },
    });
  },
};
