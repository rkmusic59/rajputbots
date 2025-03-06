import random
import requests
import asyncio
import html
from pyrogram import filters
from pyrogram.enums import PollType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SONALI_MUSIC import app

# Track quiz loops and active polls per user
quiz_loops = {}
active_polls = {}  # To track active poll messages for each user

# Function to fetch a quiz question from the API
async def fetch_quiz_question():
    categories = [9, 17, 18, 20, 21, 27]  # Quiz categories
    url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
    
    try:
        response = requests.get(url).json()
        question_data = response["results"][0]

        question = html.unescape(question_data["question"])
        correct_answer = html.unescape(question_data["correct_answer"])
        incorrect_answers = [html.unescape(ans) for ans in question_data["incorrect_answers"]]

        all_answers = incorrect_answers + [correct_answer]
        random.shuffle(all_answers)

        cid = all_answers.index(correct_answer)
        return question, all_answers, cid
    except Exception as e:
        print(f"Error fetching quiz question: {e}")
        return None, None, None

# Function to send a quiz poll with an open_period for countdown
async def send_quiz_poll(client, chat_id, user_id, interval):
    question, all_answers, cid = await fetch_quiz_question()

    if not question or not all_answers:
        print("Skipping quiz due to invalid question data.")
        return

    # Delete the previous active poll if it exists
    if user_id in active_polls:
        try:
            await app.delete_messages(chat_id=chat_id, message_ids=active_polls[user_id])
        except Exception as e:
            print(f"Failed to delete previous poll: {e}")

    # Send new quiz poll
    try:
        poll_message = await app.send_poll(
            chat_id=chat_id,
            question=question,
            options=all_answers,
            is_anonymous=False,
            type=PollType.QUIZ,
            correct_option_id=cid,
            open_period=interval
        )
        if poll_message:
            active_polls[user_id] = poll_message.id
    except Exception as e:
        print(f"Error sending poll: {e}")

# /quiz command
@app.on_message(filters.command(["quiz", "uiz"], prefixes=["/", "!", ".", "Q", "q"]))
async def quiz_info(client, message):
    await message.reply_text(
        "**Welcome to the Quiz Bot!**\n\n"
        "📌 **How it works:**\n"
        "1. Use `/quizon` to start a quiz loop.\n"
        "2. Choose a time interval (30s, 1min, 5min, 10min).\n"
        "3. A new quiz will be sent automatically at the chosen interval.\n"
        "4. Use `/quizoff` to stop the quiz loop anytime.\n\n"
        "✅ **Commands:**\n"
        "• `/quizon` - Start the quiz\n"
        "• `/quizoff` - Stop the quiz"
    )

# /quiz on command
@app.on_message(filters.command(["quizon", "uizon"], prefixes=["/", "!", ".", "Q", "q"]))
async def quiz_on(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("30s", callback_data="30_sec"), InlineKeyboardButton("1min", callback_data="1_min")],
        [InlineKeyboardButton("5min", callback_data="5_min"), InlineKeyboardButton("10min", callback_data="10_min")]
    ])

    await message.reply_text(
        "**Choose the quiz interval:**\n"
        "- 30s: Every 30 seconds\n"
        "- 1min: Every 1 minute\n"
        "- 5min: Every 5 minutes\n"
        "- 10min: Every 10 minutes\n\n"
        "🔴 Use `/quizoff` to stop the quiz anytime.",
        reply_markup=keyboard
    )

# Handle time interval selection
@app.on_callback_query(filters.regex(r"^\d+_sec$|^\d+_min$"))
async def start_quiz_loop(client, callback_query):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id

    if user_id in quiz_loops:
        await callback_query.answer("Quiz is already running!", show_alert=True)
        return

    interval_mapping = {
        "30_sec": (30, "30 seconds"),
        "1_min": (60, "1 minute"),
        "5_min": (300, "5 minutes"),
        "10_min": (600, "10 minutes")
    }

    interval, interval_text = interval_mapping.get(callback_query.data, (60, "1 minute"))

    await callback_query.answer("Quiz started!", show_alert=True)
    await callback_query.message.delete()
    await callback_query.message.reply_text(f"✅ Quiz loop started! A new quiz will be sent every {interval_text}.")

    quiz_loops[user_id] = True  # Mark loop as running

    while quiz_loops.get(user_id, False):
        await send_quiz_poll(client, chat_id, user_id, interval)
        for _ in range(interval):
            if not quiz_loops.get(user_id, False):
                return
            await asyncio.sleep(1)

# /quiz off command
@app.on_message(filters.command(["quizoff", "uizoff"], prefixes=["/", "!", ".", "Q", "q"]))
async def stop_quiz(client, message):
    user_id = message.from_user.id

    if user_id not in quiz_loops:
        await message.reply_text("⚠ No active quiz loop.")
        return

    quiz_loops.pop(user_id)
    await message.reply_text("⛔ Quiz loop stopped!")

    if user_id in active_polls:
        try:
            await app.delete_messages(chat_id=message.chat.id, message_ids=active_polls[user_id])
            active_polls.pop(user_id)
        except Exception as e:
            print(f"Failed to delete active poll: {e}")

# Help section
__MODULE__ = "Quiz"
__HELP__ = """
📌 **Quiz Bot Help**
- Use `/quizon` to start the quiz loop. You will be asked to select a time interval.
- Use `/quizoff` to stop the quiz loop anytime.
- The bot will automatically send a quiz at the chosen interval.
"""
