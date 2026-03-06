# X Reply Bot - Research & Architecture

## TwitterAPI.io Overview

**TwitterAPI.io** is a Twitter/X API wrapper that provides:
- **Endpoints**:
  - `GET /tweets/{id}` - Fetch tweet details by ID
  - `POST /tweets` - Post tweets and replies
  - Support for expansions and field parameters

**Key Features**:
- Bearer token or API key authentication
- No complex OAuth flows
- Support for media and replies
- Real-time data access
- Flexible authentication options

## Architecture Plan

### Project Structure
```
x-reply-bot/
├── bot/                          # Core bot logic
│   ├── main.py                   # Entry point
│   ├── telegram_handler.py        # Telegram Bot API integration
│   ├── twitter_api_client.py      # TwitterAPI.io wrapper
│   ├── ai_generator.py            # ChatGPT-4o integration
│   ├── ocr_processor.py           # Tesseract OCR
│   ├── reply_styles.py            # Reply style templates
│   └── utils.py                   # Helper functions
├── config/
│   ├── settings.py                # Configuration management
│   └── constants.py               # Constants and enums
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── README.md                      # Documentation
└── LICENSE                        # MIT License
```

### Technology Stack
- **Telegram**: python-telegram-bot library
- **X API**: TwitterAPI.io (REST API via requests)
- **AI**: OpenAI ChatGPT-4o API
- **OCR**: Tesseract OCR via pytesseract
- **Language**: Python 3.9+

### Workflow
1. User sends `/reply` command with text, link, or image
2. Bot processes input:
   - Text: Use directly
   - Link: Extract tweet ID and fetch via TwitterAPI.io
   - Image: Run Tesseract OCR to extract text
3. Bot prompts user for:
   - Reply style (GenZ, professional, casual, sarcastic, motivational)
   - Length (short, medium, long, custom word count)
   - Language (English, Urdu, Japanese, etc.)
4. Send to ChatGPT-4o with all parameters
5. Generate multiple reply options
6. Display options in Telegram
7. User selects one to post back to X via TwitterAPI.io

### Key Components

#### Telegram Handler
- `/start` - Initialize bot
- `/reply` - Main command to generate replies
- Button callbacks for style/length selection
- Reply option selection and posting

#### TwitterAPI.io Client
- Fetch tweet by URL or ID
- Post reply to tweet
- Handle authentication and errors

#### AI Generator
- System prompt with style and language context
- Generate multiple reply variations
- Validate response format

#### OCR Processor
- Download image from Telegram
- Run Tesseract OCR
- Clean and validate extracted text

#### Reply Styles
- GenZ: Casual, trendy, emoji-heavy
- Professional: Formal, business-appropriate
- Casual: Friendly, conversational
- Sarcastic: Witty, ironic tone
- Motivational: Inspirational, uplifting

## Dependencies
- `python-telegram-bot` - Telegram Bot API
- `requests` - HTTP client for TwitterAPI.io
- `openai` - ChatGPT-4o integration
- `pytesseract` - OCR wrapper
- `Pillow` - Image processing
- `python-dotenv` - Environment variables
- `pydantic` - Data validation

## Environment Variables
- `TELEGRAM_BOT_TOKEN` - Telegram Bot API token
- `TWITTER_API_KEY` - TwitterAPI.io API key
- `TWITTER_API_BEARER_TOKEN` - TwitterAPI.io bearer token (alternative)
- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_MODEL` - Model name (gpt-4o)
- `TESSERACT_PATH` - Path to Tesseract binary (optional)

## Next Steps
1. Set up project structure
2. Implement core modules
3. Test each component
4. Create comprehensive documentation
5. Push to GitHub
