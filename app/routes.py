from flask import Blueprint, request, render_template, send_file
from .converter import convert_excel_to_json
from werkzeug.utils import secure_filename
import os
import shutil

main = Blueprint("main", __name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
JSON_FOLDER = os.path.join(BASE_DIR, "generated_json")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(JSON_FOLDER, exist_ok=True)

def clear_folder(folder_path):
    for item in os.listdir(folder_path):
        path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"Erro ao limpar pasta {folder_path}: {e}")

@main.route("/", methods=["GET"])
def index():
    clear_folder(UPLOAD_FOLDER)
    clear_folder(JSON_FOLDER)
    return render_template("index.html")

@main.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files.get("file")
    if not uploaded_file or uploaded_file.filename == '':
        return "Nenhum arquivo selecionado", 400

    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    uploaded_file.save(filepath)

    zip_file_path = convert_excel_to_json(filepath, JSON_FOLDER)

    return send_file(zip_file_path, as_attachment=True, download_name='arquivos_json.zip')
