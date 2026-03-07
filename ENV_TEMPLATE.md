# ARC Reply - Environment Variables Configuration

This document describes all environment variables required for ARC Reply deployment.

## Local Development (.env file)

Copy the template below to `.env` file in project root:

```env
# ============================================
# TELEGRAM BOT CONFIGURATION
# ============================================
# Get from BotFather on Telegram (@BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# ============================================
# TWITTER API CONFIGURATION
# ============================================
# Get from https://api.twitter-api.io
# Use either TWITTER_API_KEY or TWITTER_API_BEARER_TOKEN (not both)
TWITTER_API_KEY=your_twitter_api_key_here
# TWITTER_API_BEARER_TOKEN=your_twitter_api_bearer_token_here

# ============================================
# GROQ API CONFIGURATION
# ============================================
# Get from https://console.groq.com
GROQ_API_KEY=your_groq_api_key_here

# ============================================
# OPTIONAL CONFIGURATION
# ============================================
# Tesseract OCR path (if not in system PATH)
# TESSERACT_PATH=/usr/bin/tesseract

# Bot admin ID for special features
# BOT_ADMIN_ID=your_telegram_user_id_here

# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# ============================================
# CLOUDFLARE WORKERS CONFIGURATION
# ============================================
# Deployment environment: local, staging, production
ENVIRONMENT=local

# Webhook URL for Telegram (set after deployment)
# WEBHOOK_URL=https://arc-reply.yourdomain.com/webhook
```

---

## Cloudflare Workers Secrets

Set secrets using Wrangler CLI:

```bash
# Set Telegram Bot Token
wrangler secret put TELEGRAM_BOT_TOKEN

# Set Twitter API Key
wrangler secret put TWITTER_API_KEY

# Set Groq API Key
wrangler secret put GROQ_API_KEY
```

Or set via Cloudflare Dashboard:
1. Go to Workers → Your Worker → Settings
2. Click "Add variable" under Secrets
3. Enter secret name and value

---

## Environment Variables Reference

### Required Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `TELEGRAM_BOT_TOKEN` | BotFather | Telegram Bot API token for authentication |
| `TWITTER_API_KEY` | TwitterAPI.io | API key for fetching tweets and posting replies |
| `GROQ_API_KEY` | Groq Console | API key for AI-powered reply generation |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | local | Deployment environment (local/staging/production) |
| `LOG_LEVEL` | INFO | Logging verbosity level |
| `TESSERACT_PATH` | system PATH | Path to Tesseract OCR binary |
| `BOT_ADMIN_ID` | none | Telegram user ID for admin features |
| `WEBHOOK_URL` | auto-detected | Telegram webhook URL |

---

## Getting API Credentials

### 1. Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create bot
4. Copy the bot token provided

**Example token format:** `123456789:ABCdefGHIjklmnoPQRstuvWXYZabcdefg`

### 2. TwitterAPI.io Key

1. Visit https://api.twitter-api.io
2. Sign up for account
3. Go to Dashboard → API Keys
4. Generate new API key
5. Copy the key

**Example key format:** `api_key_xxxxxxxxxxxxxxxxxxxxxxxx`

### 3. Groq API Key

1. Visit https://console.groq.com
2. Sign up or log in
3. Go to API Keys section
4. Create new API key
5. Copy the key

**Example key format:** `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## Environment-Specific Configuration

### Local Development

```env
ENVIRONMENT=local
LOG_LEVEL=DEBUG
TELEGRAM_BOT_TOKEN=your_test_token
TWITTER_API_KEY=your_test_key
GROQ_API_KEY=your_test_key
```

### Staging Deployment

```env
ENVIRONMENT=staging
LOG_LEVEL=INFO
# Use staging API keys if available
```

### Production Deployment

```env
ENVIRONMENT=production
LOG_LEVEL=WARN
# Use production API keys
```

---

## Security Best Practices

1. **Never commit secrets to Git:**
   - Add `.env` to `.gitignore`
   - Use `wrangler secret` for Cloudflare

2. **Rotate secrets regularly:**
   - Change API keys every 3-6 months
   - Immediately rotate if compromised

3. **Use separate keys per environment:**
   - Local: Development keys
   - Staging: Test keys
   - Production: Production keys

4. **Monitor API usage:**
   - Check API dashboards regularly
   - Set up usage alerts

---

## Troubleshooting

### "Invalid API Key" Error

1. Verify key is correct (no extra spaces)
2. Check key hasn't expired
3. Confirm key has required permissions
4. Try regenerating the key

### "Webhook not receiving updates"

1. Verify `TELEGRAM_BOT_TOKEN` is correct
2. Check webhook URL is accessible
3. Ensure webhook is set in Telegram:
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
   ```

### Environment variables not loading

1. Verify `.env` file exists in project root
2. Check variable names match exactly
3. Restart bot after changing `.env`
4. For Cloudflare: Redeploy after setting secrets

---

## Next Steps

1. Set up local `.env` file with your credentials
2. Test bot locally: `python bot/main.py`
3. Deploy to Cloudflare Workers
4. Set secrets in Cloudflare Dashboard
5. Configure Telegram webhook
6. Monitor logs and test functionality

---

For more information, see:
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [TwitterAPI.io Documentation](https://api.twitter-api.io)
- [Groq API Documentation](https://console.groq.com)
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
