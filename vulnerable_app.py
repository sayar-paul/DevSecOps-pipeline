from flask import Flask, request, render_template_string
import requests, ast, os

app = Flask(name)

OLLAMA_URL = "http://localhost:11434/api/chat"

@app.route("/", methods=["GET", "POST"])
def chat():
    response = ""

    if request.method == "POST":
        prompt = request.form.get("prompt", "")

        try:
            result = requests.post(
                OLLAMA_URL,
                json={
                    "model": "llama3",
                    "messages": [
                       
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False
                },
                timeout=180
            )

            result.raise_for_status()
            response = result.json()["message"]["content"]

        except requests.RequestException as e:
            response = f"Error connecting to Ollama: {e}"

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vulnerable AI Chat App</title>
    </head>
    <body>
        <h1>Vulnerable AI Chat App</h1>

        <form method="post">
            <input type="text" name="prompt"
                   style="width:400px"
                   placeholder="Enter your prompt">
            <input type="submit" value="Send">
        </form>

        <h3>LLM Response:</h3>
        <p>{{ response }}</p>
    </body>
    </html>
    """, response=response)

def safe_calculate(expression):
    return ast.literal_eval(expression)

SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT","You are a helpful AI assistant.")

if name == "main":
    app.run(host="127.0.0.1", port=5000, debug=False)
