from typing import Any
from flask import Flask, request, send_from_directory, Response  # type: ignore
import os

DIR = os.path.dirname(os.path.realpath(__file__))
CDN_DIR: str = f"{DIR}/cdn"
SERVER_ADDR: tuple[str, int] = "127.0.0.1", 8000
app = Flask(__name__)


@app.route("/")
def index() -> Response:
    return send_from_directory("", "index.html")


@app.route("/cdn/<path:filename>")
def serve_image(filename: str) -> Response:
    return send_from_directory("cdn", filename)


@app.route("/upload", methods=["POST"])
def upload_image() -> tuple[str, int]:
    if "image" not in request.files:
        return "No image provided", 400

    image_file: Any = request.files["image"]

    if image_file.filename == "":
        return "Invalid image filename", 400

    image_path: str = f"{CDN_DIR}/{image_file.filename}"
    image_file.save(image_path)
    return "Image uploaded successfully", 200


if __name__ == "__main__":
    if not os.path.exists(CDN_DIR):
        os.mkdir(CDN_DIR)

    app.run(host="0.0.0.0", port=8000)
