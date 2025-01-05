from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # Set this as an environment variable
bot = Bot(token=BOT_TOKEN)

# Application setup
application = ApplicationBuilder().token(BOT_TOKEN).build()


@app.post("/")
async def handle_webhook(request: Request):
    """Handle incoming webhook requests."""
    update = Update.de_json(await request.json(), bot)
    await application.process_update(update)
    return {"status": "ok"}

# Handle /start command
async def start_command(update: Update, context: CallbackContext):
    if update.message.chat.id == int(ADMIN_CHAT_ID):
        # Message for the admin
        await update.message.reply_text(
            "Welcome, Admin! To reply to user messages, use the command:\n/reply <USER_ID> <YOUR_REPLY>"
        )
    else:
        # Message for regular users
        await update.message.reply_text("Hello! Send me a message, and I'll make sure the admin gets it.")

# When a user sends a message to the bot
async def handle_user_message(update: Update, context: CallbackContext):
    user_id = update.message.chat.id
    message_text = update.message.text
    user_name = update.message.chat.username or update.message.chat.first_name

    # Forward the message to the admin
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Message from {user_name} (ID: {user_id}):\n{message_text}"
    )

# Handle the /reply command from the admin
async def reply_command(update: Update, context: CallbackContext):
    # Check if the sender is the admin
    if update.message.chat.id != int(ADMIN_CHAT_ID):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Check if the command has enough arguments
    if len(context.args) < 2:
        await update.message.reply_text(
            "Invalid format. Use the command as follows:\n/reply <USER_ID> <YOUR_REPLY>"
        )
        return

    try:
        # Extract user ID and reply message
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])

        # Send the reply to the user
        await context.bot.send_message(chat_id=user_id, text=reply_text)
        await update.message.reply_text("Message sent!")
    except Exception as e:
        await update.message.reply_text(f"Failed to send message: {e}")

def main():
    # Initialize the bot application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Set up handlers
    app.add_handler(CommandHandler("start", start_command))  # Add the /start command handler
    app.add_handler(CommandHandler("reply", reply_command))  # Add the /reply command handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.Chat(chat_id=ADMIN_CHAT_ID), handle_user_message))
