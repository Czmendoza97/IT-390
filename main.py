import requests
from flask import Flask, render_template, jsonify, request
import openai

app = Flask(__name__)

# Load API key from environment variable or configuration file
openai.api_key = "----"

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/result", methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        output = request.form.to_dict()
        name = output.get("name", "")
        return render_template("index.html", name=name)
    return render_template("index.html")

@app.route("/generate_image", methods=['POST'])
def generate_image():
    prompt = request.form.get("prompt")
    style = request.form.get("style")

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    if style not in {"vintage", "realistic"}:
        return jsonify({"error": "Invalid style."}), 400

    try:
        prompt += f" {style}"  # Append style to prompt

        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )

        image_url = response.get('data', [])[0].get('url')

        print("Generated image URL:", image_url)  # Debug statement

        # Return the image URL as JSON
        return jsonify({"image_url": image_url})

    except Exception as e:
        print("Error:", e)  # Debug statement
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
