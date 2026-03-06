import google.generativeai as genai
import PIL.Image
import io

def create_client(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-3-flash-preview")

def chat_text(client, message, history):
    try:
        formatted = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted.append({"role": role, "parts": [msg["content"]]})
        chat = client.start_chat(history=formatted)
        response = chat.send_message(message)
        return response.text, None
    except Exception as e:
        return None, str(e)

def chat_image(client, image_bytes, mime_type, question, history):
    try:
        image = PIL.Image.open(io.BytesIO(image_bytes))
        response = client.generate_content([question, image])
        return response.text, None
    except Exception as e:
        return None, str(e)
