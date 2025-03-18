import random
import requests
import time
import html  # HTML entities को डिकोड करने के लिए

from pyrogram import filters
from pyrogram.enums import PollType, ChatAction
from SONALI_MUSIC import app

last_command_time = {}


@app.on_message(filters.command(["quiz"]))
async def quiz(client, message):
    user_id = message.from_user.id
    current_time = time.time()

    # 5 सेकंड कूलडाउन
    if user_id in last_command_time and current_time - last_command_time[user_id] < 5:
        await message.reply_text("कृपया 5 सेकंड रुकें और फिर से कमांड का उपयोग करें।")
        return

    last_command_time[user_id] = current_time

    categories = [9, 17, 18, 20, 21, 27]
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)

    try:
        url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
        response = requests.get(url, timeout=10).json()

        if response["response_code"] != 0:
            await message.reply_text("❌ कोई प्रश्न प्राप्त करने में समस्या हुई। कृपया पुनः प्रयास करें।")
            return

        question_data = response["results"][0]
        question = html.unescape(question_data["question"])  # HTML एन्कोडिंग ठीक करना
        correct_answer = html.unescape(question_data["correct_answer"])
        incorrect_answers = [html.unescape(ans) for ans in question_data["incorrect_answers"]]

        all_answers = incorrect_answers + [correct_answer]
        random.shuffle(all_answers)

        correct_index = all_answers.index(correct_answer)

        await app.send_poll(
            chat_id=message.chat.id,
            question=question,
            options=all_answers,
            is_anonymous=False,
            type=PollType.QUIZ,
            correct_option_id=correct_index,
        )

    except requests.exceptions.RequestException:
        await message.reply_text("⚠️ API से डेटा प्राप्त करने में समस्या हो रही है। कृपया बाद में पुनः प्रयास करें।")
