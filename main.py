import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from search_utils import get_google_results

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Your Token
TOKEN = "8418027556:AAEIeaPSshfTSkH5D7Rjwj2RkoaIXKQMCYk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Hello {user}! 🐼\nI am **PandaForYouBot**.\n\nSend me any keyword or sentence, and I will search it on Google for you!\n\n/help - Show help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Simply type what you want to search for, and I'll find it!\nExample:\n`python tutorial`\n`/search best pizza`",
        parse_mode='Markdown'
    )

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search for the user's text message."""
    query = update.message.text
    if not query:
        return

    # Let user know we are searching
    status_msg = await context.bot.send_message(chat_id=update.effective_chat.id, text="🐼 Searching Google...")

    # Perform search
    results = get_google_results(query)

    # Edit the status message with results (or send new if too long, but edit is cleaner)
    # Telegram has a limit of 4096 chars.
    if len(results) > 4000:
        results = results[:4000] + "...(truncated)"

    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=status_msg.message_id,
        text=results,
        parse_mode='Markdown' # Using Markdown for links
    )

async def command_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle explicit /search command."""
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a query after /search. Example: `/search Panda`")
        return
    
    query = " ".join(context.args)
    
    status_msg = await context.bot.send_message(chat_id=update.effective_chat.id, text="🐼 Searching Google...")
    results = get_google_results(query)
    
    if len(results) > 4000:
        results = results[:4000] + "..."

    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=status_msg.message_id,
        text=results,
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    search_cmd_handler = CommandHandler('search', command_search)
    
    # Handle any text that is NOT a command
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_search)
    
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(search_cmd_handler)
    application.add_handler(msg_handler)
    
    print("Bot is running...")
    application.run_polling()
