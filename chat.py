import os
import google.generativeai as genai
from flask import Flask, request, render_template
import datetime

app = Flask(__name__)

    # 1. API Key setup (environment variable method)
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        exit()

genai.configure(api_key=api_key)

    # 2. Choose Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-001')

@app.route("/", methods=["GET", "POST"])
def index():
        current_year = datetime.datetime.now().year
        if request.method == "POST":
            user_prompt = request.form["prompt"]
            try:
                response = model.generate_content(user_prompt)
                return render_template("index.html", prompt=user_prompt, response=response.text, current_year=current_year)
            except Exception as e:
                 return render_template("index.html", prompt=user_prompt, error=str(e), response="", current_year=current_year)
        return render_template("index.html", prompt="", response="", current_year=current_year)

if __name__ == "__main__":
        port = int(os.environ.get('PORT', 8080))
        app.run(debug=True, host='0.0.0.0', port=port)