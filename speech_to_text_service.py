from flask import Flask, request, jsonify
import speech_recognition as sr
import base64
import os
from flask_cors import CORS
from pydub import AudioSegment
import io

app = Flask(__name__)
CORS(app)

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    try:
        audio_base64 = request.json.get('audio_base64')
        if not audio_base64:
            return jsonify({"error": "No audio provided"}), 400

        # Decodifica el archivo de audio base64
        audio_data = base64.b64decode(audio_base64)
        audio_path = "/var/www/translator/traductor-de-voz-a-texto/tmp_audio/temp_audio.wav"

        # audio_path = "/tmp/temp_audio.wav"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(audio_data)

        # Inicializa el recognizer de SpeechRecognition
        recognizer = sr.Recognizer()

        # Lee el archivo de audio usando SpeechRecognition
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        # Intenta reconocer el texto en el audio
        try:
            text = recognizer.recognize_google(audio, language="es-ES")  # Cambia el idioma si es necesario
        except sr.UnknownValueError:
            return jsonify({"error": "No se pudo entender el audio"}), 400
        except sr.RequestError as e:
            return jsonify({"error": f"Error con el servicio de reconocimiento: {str(e)}"}), 500
        finally:
            # Elimina el archivo de audio temporal
            os.remove(audio_path)

        return jsonify({"text": text}), 200
    except Exception as e:
        print(f"Error procesando el audio: {str(e)}")  # Log en el servidor
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)