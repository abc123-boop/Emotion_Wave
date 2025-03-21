from flask import Flask, render_template, request, jsonify
import os
import torch
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from model import EmotionModel  # Import your trained model class
from prepare_data import extract_features  # Ensure this function is implemented correctly

app = Flask(__name__)

# Define upload directory
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed_audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load trained model
MODEL_PATH = "emotion_model.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EmotionModel().to(device)  
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

# Emotion labels (Ensure they match your model's output classes)
EMOTIONS = ["angry", "calm", "disgust", "fearful", "happy", "neutral", "sad", "surprised"]

def convert_to_wav(input_path):
    """Convert any audio format to WAV (16kHz, mono)."""
    filename = os.path.basename(input_path).rsplit(".", 1)[0]  # Remove extension
    output_path = os.path.join(PROCESSED_FOLDER, f"{filename}.wav")

    try:
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_frame_rate(16000).set_channels(1)  # Ensure 16kHz mono
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        print(f"❌ Error converting audio: {e}")
        return None

def predict_emotion(audio_path):
    try:
        features = extract_features(audio_path)
        if features is None:
            return "error"

        # Convert to tensor and ensure correct shape (batch_size, 40)
        features = torch.tensor(features).float().unsqueeze(0).to(device)  # Shape: (1, 40)

        # Predict emotion
        with torch.no_grad():
            logits = model(features)

        predicted_class = torch.argmax(logits, dim=-1).item()
        predicted_emotion = EMOTIONS[predicted_class] if predicted_class < len(EMOTIONS) else "unknown"

        return predicted_emotion
    
    except Exception as e:
        print(f"❌ Error processing audio: {e}")
        return "error"


@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    """Handle audio file upload and emotion prediction."""
    if "audio" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["audio"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    original_filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(original_filepath)

    # Convert to WAV if necessary
    if not file.filename.lower().endswith(".wav"):
        converted_filepath = convert_to_wav(original_filepath)
        if not converted_filepath:
            return jsonify({"error": "Audio conversion failed"}), 500
    else:
        converted_filepath = original_filepath

    # Predict emotion
    emotion = predict_emotion(converted_filepath)

    return jsonify({"emotion": emotion})

if __name__ == "__main__":
    app.run(debug=True)

