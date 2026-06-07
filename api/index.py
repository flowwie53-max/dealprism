from flask import Flask, render_template
import pandas as pd
from scraper import get_top_deals

app = Flask(__name__, template_folder='../templates')

@app.route("/")
def index():
    data = get_top_deals()
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values(by="Est. Profit £", ascending=False)
        results = df.to_html(classes='table table-striped', index=False, escape=False)
    else:
        results = "<p>Failed to load deals. Refresh the page.</p>"

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
