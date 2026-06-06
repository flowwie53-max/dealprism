from flask import Flask, render_template, request
import pandas as pd
from scraper import scrape_argos, scrape_ebay, scrape_currys

app = Flask(__name__, template_folder='../templates')

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    query = ""
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        argos = scrape_argos(query)
        ebay = scrape_ebay(query)
        currys = scrape_currys(query)
        
        all_products = argos + ebay + currys
        if all_products:
            df = pd.DataFrame(all_products)
            df = df.sort_values(by="price", ascending=True)
            results = df.to_html(classes='table table-striped', index=False, escape=False)
        else:
            results = "<p>No results found. Try a different search term.</p>"
    
    return render_template("index.html", results=results, query=query)

application = app

if __name__ == "__main__":
    app.run(debug=True)
