from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import eyed3
from werkzeug.utils import secure_filename

app = Flask(__name__)

CORS(app, resources={r"/*": {"methods": ["GET", "POST"]}})


@app.route('/')
def index():
  return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


@app.route('/list_files', methods=['GET'])
def list_files():
  try:
    files = os.listdir('/files')
    return jsonify({"files": files}), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():

  upload_directory = '/files'

  if 'file' not in request.files:
    return jsonify({"error": "No file part"})

  file = request.files['file']

  if file.filename == '':
    return jsonify({"error": "No file selected"})

  # Your naming convention
  name = request.form.get('name', 'Unknown Show')
  dateOfAir = request.form.get('dateOfAir', 'Unknown Date')
  description = request.form.get('description', 'Unknown Description')

  if file:
    new_filename = f"{name} - {dateOfAir} ({description}).mp3"

    # Secure and save the file
    secure_name = secure_filename(new_filename)
    file_path = os.path.join(upload_directory, secure_name)
    file.save(file_path)

    # Update Metadata here if needed

    return jsonify({
        "success": True,
        "message": f"File saved as {new_filename}"
    })


if __name__ == '__main__':
  app.run(debug=True, port=os.getenv("PORT", default=5000))
