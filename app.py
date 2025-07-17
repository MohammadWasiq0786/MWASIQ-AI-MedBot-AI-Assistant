from flask import Flask, render_template, request, jsonify
from euriai import EuriaiClient 
from dotenv import load_dotenv 
import os 

#load environment
load_dotenv()
api_key = os.getenv("EURI_API_KEY")

#Euri client 
client = EuriaiClient(
    api_key = api_key,
    model = "gpt-4.1-nano"
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error":"Message is required"}), 400

        #Euri prompt
        prompt =  f"You are a helpful medical assistant. Be informative but encourage users to consult a real doctor. Here is the user question:\n\n{user_message}"
        response = client.generate_completion(
            prompt=prompt,
            temperature=0.7,
            max_tokens=300
        )

        reply = response['choices'][0]['message']['content']

        return jsonify({"response": reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug=True)