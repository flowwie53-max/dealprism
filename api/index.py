from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder='../templates')

@app.route("/")
def index():
    results = """
    <h2>Argos Top Deals Mode</h2>
    <p>Scraping is currently limited due to serverless timeout.</p>
    <p>We'll either:</p>
    <ul>
        <li>Use caching (next version)</li>
        <li>Move to better hosting</li>
    </ul>
    <br>
    <p><strong>Current status: Working on a stable solution.</strong></p>
    """
    return render_template("index.html", results=results)

application = app

if __name__ == "__main__":
    app.run(debug=True)
