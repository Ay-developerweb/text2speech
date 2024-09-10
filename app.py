from flask import Flask, render_template, request, flash, redirect
from gtts import gTTS
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

@app.route('/')
def ai():
    return render_template("first.html")

@app.route('/index', methods=['GET', 'POST'])
def index():
    text = ""  # Default empty text
    audio_path = os.path.join('static', 'audio.mp3')  # Define the audio file path
    
    if request.method == 'POST':
        text = request.form['text']
        
        if text.strip():  # Only proceed if there's text to convert
            try:
                # Delete the existing audio file if it exists
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                    
                # Generate a new audio file
                tts = gTTS(text)
                tts.save(audio_path)
                return render_template("index.html", audio_generated=True, text=text)
            
            except Exception as e:
                # Handle gTTS exceptions (e.g., no internet connection)
                flash("Failed to generate audio. Connect to the internet by turning on your data connection.", "error")
        
        return render_template("index.html", audio_generated=False, text=text)
    
    return render_template("index.html", audio_generated=False, text=text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
