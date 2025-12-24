import sys
import os
import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import TOKEN, register_handlers

app = Flask(__name__)

# Initialize bot app globally to reuse
bot_app = ApplicationBuilder().token(TOKEN).build()
register_handlers(bot_app)

@app.route('/', methods=['GET'])
def index():
    return "PandaForYouBot is running!"

@app.route('/webhook', methods=['POST'])
async def webhook(): # Flask 2.0+ supports async routes if extra[async] or similar, but Vercel might vary.
    # Standard approach for sync WSGI running async code
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        
        # We need to await the process_update.
        # Since we are in an async function (if supported) or need to run loop.
        # Vercel python runtime handles WSGI. 
        # If we define this as 'async def', we need a WSGI server that supports it or Vercel's handling.
        # Safest way for standard WSGI on Vercel:
        
        async with bot_app:
            await bot_app.process_update(update)
            
        return "OK"
    return "OK"

# Vercel requires the app (Flask instance) to be exposed as 'app' or handler
