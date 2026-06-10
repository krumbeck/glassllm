import os
import math
from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables and initialize OpenAI
load_dotenv()
client = OpenAI()

app = Flask(__name__)

# Define route for GET and POST requests
@app.route("/", methods=["GET", "POST"])
def index():
    erg_daten = None
    fehler = None
    user_prompt = ""
    # standard value for creativity
    temperature = 1.0 

    if request.method == "POST":
        # Get the text and the temperature from the input fields
        user_prompt = request.form.get("prompt", "")
        
        
        try:
            temperature = float(request.form.get("temperature", 1.0))
        except ValueError:
            temperature = 1.0
        
        if user_prompt.strip() == "":
            fehler = "Please enter a sentence!"
        else:
            try:
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": f"Complete the sentence with only one word: {user_prompt}"}
                    ],
                    logprobs=True,
                    top_logprobs=3,
                    max_tokens=5,
                    temperature=temperature  # pass value to OpenAI
                )

                erg_daten = []
                token_logprobs = response.choices[0].logprobs.content

                # outer loop goes through every token
                for info in token_logprobs:
                    alternativen = []
                    
                    # inner loop gets top3 options for that token 
                    for top_option in info.top_logprobs:
                        prozent = math.exp(top_option.logprob) * 100
                        alternativen.append({
                            "token": top_option.token,
                            "wahrscheinlichkeit": f"{prozent:.2f}",
                            "raw_prob": prozent  
                        })
                    
                    
                    erg_daten.append({
                        "wort_fragment": info.token,
                        "top_optionen": alternativen
                    })

            except Exception as e:
                fehler = f"API Error: {e}"

    
    return render_template("index.html", results=erg_daten, error=fehler, prompt=user_prompt, temperature=temperature)
    


if __name__ == "__main__":
    app.run(debug=True)