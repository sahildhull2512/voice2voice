# server.py
from quart import Quart, websocket
from openai import OpenAI
import tempfile
import dotenv
import os
import ffmpeg

dotenv.load_dotenv()

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Quart(__name__)

@app.websocket('/ws')
async def ws():
    while True:
        data = await websocket.receive()
        print(f"🟢 Received {len(data)} bytes")
        # Assume data is base64 encoded audio chunk
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_webm:
            tmp_webm.write(data)
            tmp_webm.flush()

            tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

            # Convert .webm to .wav
            ffmpeg.input(tmp_webm.name).output(tmp_wav.name).run(overwrite_output=True)

            with open(tmp_wav.name, "rb") as audio_file:
                transcript_response = openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            user_text = transcript_response.text
            print("---------------------------------------------------")
            print(f"Transcript: {user_text}")
            print("---------------------------------------------------")

            # LLM
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Reply in a sweet and friendly way. Your name is Chintu"},
                    {"role": "user", "content": user_text}]
            )
            reply_text = response.choices[0].message.content
            print("---------------------------------------------------")
            print(f"Reply: {reply_text}")
            print("---------------------------------------------------")

            # Text to speech
            speech = openai_client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=reply_text
            )
            # Step 4: Send audio back
            await websocket.send(speech.content)

# app.run()