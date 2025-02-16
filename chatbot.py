import json
from flask import Flask, request, jsonify, send_from_directory      # Import Flask modules 
import google.generativeai as genai       # Import Google Gemini AI
from flask_cors import CORS       # Import CORS

# Create the Flask app
app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for frontend access

# Configure Google Gemini AI
API_KEY = ""  # Replace with your API key
genai.configure(api_key=API_KEY) 

# Load FAQs from a JSON file
with open("faqs.json", "r") as file:
    faq_data = json.load(file)

# Function to check if a message is in FAQs
def get_faq_answer(user_input):
    return faq_data.get(user_input, None)

# Function to chat with Gemini AI
def chat_with_gemini(user_input):   
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    return response.text


@app.route("/bot-avatar.png")
def serve_avatar():
    return send_from_directory("static", "bot-avatar.png")

# Routes
@app.route("/")
def serve_frontend():
    return send_from_directory("static", "index.html")



# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "I didn't receive any message!"})

   # Check if the question is in the FAQ database
    faq_answer = get_faq_answer(user_message)
    if faq_answer:
        return jsonify({"reply": faq_answer})

    # If not found, ask Gemini AI
    ai_reply = chat_with_gemini(user_message)
    return jsonify({"reply": ai_reply})

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
