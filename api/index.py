from flask import Flask, render_template, request
import pandas as pd
from scraper import get_comparison_data

app = Flask(__name__, template_folder='../templates')

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST" or True:  # Auto load top deals
        data = get_comparison_data()
        if data:
            df = pd.DataFrame(data)
            df = df.sort_values(by="Est. Profit", ascending=False)
            results = df.to_html(classes='table table-striped', index=False, escape=False)
    
    return render_template("index.html", results=results)

application = app

if __name__ == "__main__":
    app.run(debug=True)
