from flask import Flask, render_template
import pandas as pd
from scraper import scrape_argos_top_deals, quick_ebay_search

app = Flask(__name__, template_folder='../templates')

@app.route("/")
def index():
    data = scrape_argos_top_deals()
    results = None
    
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values(by='Est. Profit', ascending=False)
        results = df.to_html(classes='table table-striped', index=False, escape=False)
    else:
        results = "<p>Couldn't load deals right now. Try refreshing.</p>"

    return render_template("index.html", results=results)

application = app

if __name__ == "__main__":
    app.run(debug=True)
