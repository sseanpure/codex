# Morning Brew Telegram Bot

This bot fetches the latest article from [morningbrew.com](https://www.morningbrew.com/), summarizes it using OpenAI, translates the summary to Russian, and posts the result to a Telegram channel.

## Setup

1. Install dependencies:
   ```bash
   pip install python-telegram-bot openai requests beautifulsoup4
   ```
2. Set the following environment variables:
   - `OPENAI_API_KEY` – your OpenAI API key.
   - `TELEGRAM_TOKEN` – token for your Telegram bot.
   - `CHANNEL_ID` – ID or username of the Telegram channel (e.g. `@morningbrewdaily`).

   On Windows you can set them in the command prompt before running the
   script:

   ```cmd
   set OPENAI_API_KEY=your_openai_key
   set TELEGRAM_TOKEN=your_bot_token
   set CHANNEL_ID=@yourchannel
   ```

## Usage

Run the bot:

```bash
python bot.py
```

The bot posts a summary once at startup and then repeats every 24 hours.
