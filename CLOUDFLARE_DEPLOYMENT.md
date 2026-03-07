# ARC Reply - Cloudflare Workers Deployment Guide

This guide covers deploying ARC Reply as a Telegram bot webhook on Cloudflare Workers with auto-deploy from GitHub.

## Overview

ARC Reply runs as a serverless Telegram bot on Cloudflare Workers. The bot receives webhook updates from Telegram and processes them to generate AI-powered replies for X (Twitter) posts.

**Key Features:**
- ✅ Serverless deployment (no server maintenance)
- ✅ Global CDN distribution
- ✅ Auto-deploy from GitHub
- ✅ Environment-specific configurations
- ✅ Secure secret management
- ✅ Real-time logging and monitoring

---

## Prerequisites

1. **Cloudflare Account** - Free or paid tier
2. **GitHub Account** - For repository connection
3. **Telegram Bot Token** - From BotFather
4. **TwitterAPI.io Key** - For X API access
5. **Groq API Key** - For AI reply generation
6. **Node.js 18+** - For local development
7. **Wrangler CLI** - Cloudflare Workers CLI

---

## Step 1: Install Wrangler CLI

```bash
npm install -g wrangler
```

Verify installation:
```bash
wrangler --version
```

---

## Step 2: Authenticate with Cloudflare

```bash
wrangler login
```

This opens a browser to authorize Wrangler with your Cloudflare account.

---

## Step 3: Configure Wrangler Project

The project includes a `wrangler.toml` configuration file. Update it with your settings:

```toml
name = "arc-reply"
main = "worker.js"
compatibility_date = "2024-03-05"

[env.production]
name = "arc-reply-prod"
routes = [
  { pattern = "arc-reply.yourdomain.com/*", zone_name = "yourdomain.com" }
]
```

**Key configurations:**
- `name`: Worker name (must be unique)
- `main`: Entry point file
- `routes`: Custom domain routes (optional)
- `env`: Environment-specific settings

---

## Step 4: Set Environment Secrets

Set the required API keys as secrets in Cloudflare Workers:

```bash
# Set Telegram Bot Token
wrangler secret put TELEGRAM_BOT_TOKEN

# Set Twitter API Key
wrangler secret put TWITTER_API_KEY

# Set Groq API Key
wrangler secret put GROQ_API_KEY
```

When prompted, paste each secret value.

**Verify secrets are set:**
```bash
wrangler secret list
```

---

## Step 5: Deploy to Cloudflare Workers

### Option A: Deploy from Local Machine

```bash
# Deploy to production
wrangler deploy

# Or deploy to staging environment
wrangler deploy --env staging
```

### Option B: Deploy from GitHub (Recommended)

1. **Connect GitHub Repository to Cloudflare:**
   - Go to Cloudflare Dashboard → Workers → Overview
   - Click "Create a Service"
   - Select "GitHub" as source
   - Authorize Cloudflare to access your GitHub account
   - Select the `ARC-Reply` repository

2. **Configure Auto-Deploy:**
   - In Cloudflare Dashboard, go to Workers → Settings
   - Enable "GitHub auto-deploy"
   - Select branch: `main`
   - Every push to `main` triggers automatic deployment

3. **Set Secrets in Cloudflare Dashboard:**
   - Go to Workers → Settings → Secrets
   - Add each secret:
     - `TELEGRAM_BOT_TOKEN`
     - `TWITTER_API_KEY`
     - `GROQ_API_KEY`

---

## Step 6: Configure Telegram Webhook

Get your Cloudflare Workers URL:

```bash
wrangler deployments list
```

Or find it in Cloudflare Dashboard → Workers → Your Worker → Settings → Domains

**Set Telegram webhook:**

```bash
curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://arc-reply.yourdomain.com/webhook"}'
```

Replace:
- `<YOUR_BOT_TOKEN>` - Your Telegram bot token
- `https://arc-reply.yourdomain.com/webhook` - Your Cloudflare Workers webhook URL

**Verify webhook is set:**

```bash
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

---

## Step 7: Test the Deployment

### Health Check

```bash
curl https://arc-reply.yourdomain.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "bot": "ARC Reply"
}
```

### Telegram Bot Test

1. Open Telegram and find your bot
2. Send `/start` command
3. Bot should respond with welcome message
4. Send `/reply` to start generating replies

### View Logs

```bash
wrangler tail
```

This shows real-time logs from your Cloudflare Worker.

---

## Environment Variables

The bot uses the following environment variables:

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Secret | ✅ | Telegram Bot API token |
| `TWITTER_API_KEY` | Secret | ✅ | TwitterAPI.io API key |
| `GROQ_API_KEY` | Secret | ✅ | Groq API key for AI |
| `ENVIRONMENT` | Var | ❌ | Deployment environment (production/staging) |
| `LOG_LEVEL` | Var | ❌ | Logging level (debug/info/warn/error) |

---

## Webhook Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook` | POST | Telegram webhook updates |
| `/health` | GET | Health check |
| `/` | GET | Root endpoint (info) |

---

## Auto-Deploy Setup

### GitHub Integration

1. **Enable GitHub Integration:**
   - Cloudflare Dashboard → Workers → Settings
   - Click "Connect GitHub"
   - Authorize Cloudflare
   - Select `ARC-Reply` repository

2. **Configure Deployment:**
   - Branch: `main`
   - Auto-deploy: Enabled
   - Production environment: `production`

3. **Deployment Triggers:**
   - Every push to `main` branch triggers deployment
   - Deployment status visible in GitHub Actions
   - Rollback available in Cloudflare Dashboard

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Workers

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Deploy to Cloudflare
        run: npx wrangler deploy
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

---

## Monitoring & Logs

### Real-Time Logs

```bash
wrangler tail
```

### Cloudflare Dashboard

1. Go to Cloudflare Dashboard → Workers → Your Worker
2. Click "Logs" tab
3. View real-time request logs

### Error Handling

The bot includes comprehensive error handling:
- Invalid API keys → Clear error messages
- Network errors → Automatic retry
- Malformed requests → 400 Bad Request
- Server errors → 500 Internal Server Error

---

## Troubleshooting

### Webhook Not Receiving Updates

1. **Verify webhook URL:**
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
   ```

2. **Check Telegram logs:**
   - Telegram shows webhook errors if connection fails
   - Verify URL is HTTPS and publicly accessible

3. **Test webhook manually:**
   ```bash
   curl -X POST https://arc-reply.yourdomain.com/webhook \
     -H "Content-Type: application/json" \
     -d '{"update_id": 1, "message": {"text": "/start"}}'
   ```

### Secrets Not Working

1. **Verify secrets are set:**
   ```bash
   wrangler secret list
   ```

2. **Re-deploy after setting secrets:**
   ```bash
   wrangler deploy
   ```

3. **Check secret names match code:**
   - Code uses: `env.TELEGRAM_BOT_TOKEN`
   - Secret name must be: `TELEGRAM_BOT_TOKEN`

### Deployment Failures

1. **Check deployment logs:**
   ```bash
   wrangler deployments list
   ```

2. **View error details:**
   - Cloudflare Dashboard → Workers → Deployments
   - Click failed deployment for error details

3. **Rollback to previous version:**
   - Cloudflare Dashboard → Workers → Deployments
   - Click "Rollback" on previous deployment

---

## Performance Optimization

### CPU Time

- Default: 50ms CPU time limit
- Increase in `wrangler.toml` if needed:
  ```toml
  limits = { cpu_ms = 100 }
  ```

### Caching

- Telegram updates not cached (real-time)
- Static responses cached with Cloudflare CDN

### Scaling

- Cloudflare Workers automatically scales
- No manual scaling needed
- Handles millions of requests

---

## Security Best Practices

1. **Secret Management:**
   - Never commit secrets to GitHub
   - Use Cloudflare secret management
   - Rotate secrets regularly

2. **Webhook Security:**
   - Verify Telegram signature (optional)
   - Use HTTPS only
   - Restrict webhook to Telegram IPs

3. **API Keys:**
   - Use separate keys for each environment
   - Rotate keys periodically
   - Monitor API usage

---

## Cost Estimation

**Cloudflare Workers Pricing:**
- Free tier: 100,000 requests/day
- Paid tier: $0.50 per 10 million requests
- Additional costs: API calls to Telegram, TwitterAPI.io, Groq

**Typical Usage:**
- Small bot (< 1,000 users): Free tier sufficient
- Medium bot (1,000-10,000 users): ~$5-10/month
- Large bot (> 10,000 users): Custom pricing

---

## Maintenance

### Regular Tasks

1. **Monitor logs:** Check for errors weekly
2. **Update dependencies:** Run `npm update` monthly
3. **Rotate secrets:** Every 3-6 months
4. **Test webhook:** Verify connectivity weekly

### Deployment Updates

1. **Make code changes** in GitHub
2. **Commit and push** to `main` branch
3. **Auto-deploy triggers** automatically
4. **Verify deployment** in Cloudflare Dashboard

---

## Support & Resources

- **Cloudflare Workers Docs:** https://developers.cloudflare.com/workers/
- **Wrangler CLI Docs:** https://developers.cloudflare.com/workers/wrangler/
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **TwitterAPI.io Docs:** https://api.twitter-api.io
- **Groq API Docs:** https://console.groq.com

---

## Next Steps

1. ✅ Deploy to Cloudflare Workers
2. ✅ Set webhook in Telegram
3. ✅ Test bot functionality
4. ✅ Monitor logs and performance
5. ✅ Configure auto-deploy from GitHub

---

**Deployment Status:** Ready for Production

For issues or questions, refer to the troubleshooting section or check Cloudflare/Telegram documentation.
