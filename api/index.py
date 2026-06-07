from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, template_folder='../templates')

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    message = "Click the button below to load current Argos Top Deals"

    if request.method == "POST":
        # Very light version - just placeholder for now
        message = "✅ Top Deals loaded (scraping coming in next update)"
        results = "<p>Argos Top Deals mode activated.<br><br>We'll load real data without timing out in the next version.</p>"

    return render_template("index.html", results=results, message=message)

application = app

if __name__ == "__main__":
    app.run(debug=True)
