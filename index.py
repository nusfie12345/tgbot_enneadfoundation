from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

BOT_TOKEN = "7872625121:AAHsyBS5KY8KIHjLn2rqUpUjKMqg4kePme8"  # Replace with your actual bot token
ADMIN_CHAT_ID = "495221774"  # Replace with your admin chat ID
bot = Bot(token=BOT_TOKEN)

# Initialize FastAPI app
app = FastAPI()

# Initialize Telegram Application
application = ApplicationBuilder().token(BOT_TOKEN).build()

@app.post("/webhook")  # Define the webhook route
async def handle_webhook(request: Request):
    """Handle incoming POST requests from Telegram."""
    try:
        # Parse the incoming update
        data = await request.json()
        update = Update.de_json(data, bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Command: /start
async def start_command(update: Update, context: CallbackContext):
    if update.message.chat.id == int(ADMIN_CHAT_ID):
        await update.message.reply_text(
            "Welcome, Admin! Use /reply <USER_ID> <YOUR_REPLY> to communicate with users."
        )
    else:
        await update.message.reply_text("Hello! Your messages will be forwarded to the admin.")

# Handle user messages
async def handle_user_message(update: Update, context: CallbackContext):
    user_id = update.message.chat.id
    message_text = update.message.text
    user_name = update.message.chat.username or update.message.chat.first_name

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Message from {user_name} (ID: {user_id}):\n{message_text}"
    )

# Command: /reply
async def reply_command(update: Update, context: CallbackContext):
    if update.message.chat.id != int(ADMIN_CHAT_ID):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Invalid format. Use /reply <USER_ID> <YOUR_REPLY>."
        )
        return

    try:
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=reply_text)
        await update.message.reply_text("Message sent!")
    except Exception as e:
        await update.message.reply_text(f"Failed to send message: {e}")

# Main entry point to add handlers
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("reply", reply_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.Chat(chat_id=ADMIN_CHAT_ID), handle_user_message))
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

BOT_TOKEN = "bot_id_here"  # Replace with your actual bot token
ADMIN_CHAT_ID = "my_chat_id_here"  # Replace with your admin chat ID
bot = Bot(token=BOT_TOKEN)

# Initialize FastAPI app
app = FastAPI()

# Initialize Telegram Application
application = ApplicationBuilder().token(BOT_TOKEN).build()

@app.post("/webhook")  # Define the webhook route
async def handle_webhook(request: Request):
    """Handle incoming POST requests from Telegram."""
    try:
        # Parse the incoming update
        data = await request.json()
        update = Update.de_json(data, bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Command: /start
async def start_command(update: Update, context: CallbackContext):
    if update.message.chat.id == int(ADMIN_CHAT_ID):
        await update.message.reply_text(
            "Welcome, Admin! Use /reply <USER_ID> <YOUR_REPLY> to communicate with users."
        )
    else:
        await update.message.reply_text("Hello! Your messages will be forwarded to the admin.")

# Handle user messages
async def handle_user_message(update: Update, context: CallbackContext):
    user_id = update.message.chat.id
    message_text = update.message.text
    user_name = update.message.chat.username or update.message.chat.first_name

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Message from {user_name} (ID: {user_id}):\n{message_text}"
    )

# Command: /reply
async def reply_command(update: Update, context: CallbackContext):
    if update.message.chat.id != int(ADMIN_CHAT_ID):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Invalid format. Use /reply <USER_ID> <YOUR_REPLY>."
        )
        return

    try:
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=reply_text)
        await update.message.reply_text("Message sent!")
    except Exception as e:
        await update.message.reply_text(f"Failed to send message: {e}")

# Main entry point to add handlers
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("reply", reply_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.Chat(chat_id=ADMIN_CHAT_ID), handle_user_message))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="0.0.0.0", port=8000)
