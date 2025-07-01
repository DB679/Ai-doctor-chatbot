import os
import gradio as gr
from pymongo import MongoClient

from brain_of_the_doctor import encode_image, analyze_with_groq
from voice_of_patient import transcribe_with_groq
from voice_of_doctor import text_to_speech_with_elevenlabs

# Load API keys and DB URI
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["medical_ai"]
collection = db["consultations"]

# Prompt for AI doctor
system_prompt = """You have to act as a professional doctor. I know you are not, but this is for learning purposes. 
With what I see, I think you have .... Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""

# Global to track audio
last_audio_path = "final.mp3"

def process_inputs(audio_filepath, text_input, image_filepath):
    global last_audio_path

    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=GROQ_API_KEY,
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    ) if audio_filepath else None

    query = text_input or speech_to_text_output
    if not query:
        return "❌ Please provide symptoms through text or voice.", None

    encoded_image = encode_image(image_filepath) if image_filepath else None

    doctor_response = analyze_with_groq(
        query=system_prompt + query,
        encoded_image=encoded_image
    )

    last_audio_path = "final.mp3"
    text_to_speech_with_elevenlabs(doctor_response, last_audio_path)

    collection.insert_one({
        "transcription": speech_to_text_output,
        "text_input": text_input,
        "doctor_response": doctor_response
    })

    return doctor_response, last_audio_path

def replay_audio():
    global last_audio_path
    return last_audio_path

# Professional Gradio UI
with gr.Blocks(title="AI Doctor") as demo:
    gr.Markdown("<h1 style='text-align: center;'>🧠 AI Doctor - Medical Assistance via Voice, Text & Image</h1>")

    gr.Markdown(
        "<h2 style='text-align:center;'>Welcome to your AI Doctor. Please describe your symptoms by speaking, typing, or uploading an image.</h2>\n\n"
        
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 👨‍⚕️ Patient Input")
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Speak your symptoms")
            text_input = gr.Textbox(lines=3, placeholder="Or type your symptoms here...", label="💬 Text Input")
            image_input = gr.Image(type="filepath", label="🖼️ Upload Image (Optional)")
            submit_btn = gr.Button("🩺 Submit")

        with gr.Column(scale=1):
            gr.Markdown("### 🩻 Doctor's Response")
            doctor_text = gr.Textbox(label="🧠 Diagnosis / Advice", lines=3)
            doctor_audio = gr.Audio(label="🔊 Doctor's Voice", type="filepath")
            replay_btn = gr.Button("🔁 Replay Voice")

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, text_input, image_input],
        outputs=[doctor_text, doctor_audio]
    )

    replay_btn.click(
        fn=replay_audio,
        inputs=[],
        outputs=doctor_audio
    )

    gr.Markdown("---")
    gr.Markdown(
        "🛡️ **Disclaimer:** This application is a simulated AI doctor for educational/demo purposes only. "
        "Always consult a qualified medical professional for actual diagnosis and treatment."
    )

if __name__ == "__main__":
    import gradio as gr
    # your launch code like:
    gr.Interface(...).launch(server_name="0.0.0.0", server_port=8080)

