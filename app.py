
from flask import Flask, request, render_template
import google.generativeai as genai
from PIL import Image
import os

from dotenv import load_dotenv

app = Flask(__name__)



api_key = os.getenv("API_KEY")
genai.configure(api_key = api_key)

model = genai.GenerativeModel("gemini-1.5-pro")

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "image" not in request.files:
            return "No image uploaded", 400

        image_file = request.files["image"]
        image = Image.open(image_file)

        # Define the AI prompt
        prompt = """You are a highly experienced radiologist with expertise in interpreting medical images..."""  # (Your detailed prompt here)

        # Send to Gemini AI
        response = model.generate_content([image, prompt])
        result_text = response.text

        return render_template("result.html", image_path=image_file.filename, result=result_text)

    return render_template("upload.html")  # Load the upload form

if __name__ == "__main__":

    # Load configuration from environment variables
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))

    app.run(debug=debug_mode, host=host, port=port)