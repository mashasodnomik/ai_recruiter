import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyBeXA5UN__Wzt9QcmjB2KEMrIspFc33tXQ")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction="ты помощник эйчар менеджера и ты помгаешь оптимизировать азадачу рекрутинга ты должен сранивать резюме и давать оценку того кого возьмешь на работу или нет\n",
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("сколько хвостов у кота")

print(response.text)