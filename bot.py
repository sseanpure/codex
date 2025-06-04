import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Updater, JobQueue
import openai
import json
import re

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')  # e.g. '@mychannel'

# Initialize APIs
openai.api_key = OPENAI_API_KEY
bot = Bot(token=TELEGRAM_TOKEN)


def fetch_morningbrew_article():
    """Fetches the latest Morning Brew newsletter as plain text."""
    url = 'https://www.morningbrew.com/daily/latest'
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    script = soup.find('script', id='__NEXT_DATA__')
    if not script or not script.string:
        return ''

    data = json.loads(script.string)
    html_content = (
        data.get('props', {})
        .get('pageProps', {})
        .get('issueData', {})
        .get('html', '')
    )
    if not html_content:
        return ''

    return BeautifulSoup(html_content, 'html.parser').get_text(separator='\n')


def summarize_and_translate(text):
    """Uses OpenAI to summarize the text and translate it to Russian."""
    if not text:
        return ''
    prompt = (
        'Summarize the following newsletter in a short paragraph and '
        'translate the summary to Russian:\n\n'
        f'{text}'
    )
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=500
    )
    return response.choices[0].message['content'].strip()


def send_summary(context):
    """Fetch article, summarize, and send to Telegram channel."""
    try:
        article_text = fetch_morningbrew_article()
        summary = summarize_and_translate(article_text)
        if summary:
            bot.send_message(chat_id=CHANNEL_ID, text=summary)
    except Exception as exc:
        print(f'Error sending summary: {exc}')


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    job_queue: JobQueue = updater.job_queue

    # Send summary once on startup
    job_queue.run_once(send_summary, 0)
    # Schedule every 24 hours
    job_queue.run_repeating(send_summary, interval=24*60*60, first=24*60*60)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
