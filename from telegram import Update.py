from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Your bot token from BotFather
TOKEN = "7872625121:AAHQbbmq54Uw0Jun4mt4lq_eLBx7JVBt8g0"

# Dictionary to store user messages and their chat IDs
user_data = {}

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Ennead Foundation! I am Ennead Bot. I will pass your message onto our leader.")

# Handle incoming messages and forward them to you
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_data

    # Store user's message and chat ID
    user_id = update.message.chat_id
    user_data[user_id] = update.message.text

    # Forward the message to you
    YOUR_USER_ID = 495221774  # Replace with your Telegram user ID
    await context.bot.send_message(
        chat_id=YOUR_USER_ID,
        text=f"New response from {user_id}: {update.message.text}"
    )

# Handle your replies to users
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    YOUR_USER_ID = 123456789  # Replace with your Telegram user ID
    if update.message.chat_id != YOUR_USER_ID:
        await update.message.reply_text("This command is restricted.")
        return

    # Extract arguments: user ID and your reply message
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /reply <user_id> <your_message>")
        return

    try:
        user_id = int(args[0])
        message = " ".join(args[1:])

        # Send the reply to the user
        await context.bot.send_message(chat_id=user_id, text=message)
        await update.message.reply_text(f"Replied to {user_id}: {message}")
    except Exception as e:
        await update.message.reply_text(f"Failed to send message: {e}")


# Main function to set up the bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("reply", reply))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
