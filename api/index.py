from flask import Flask, render_template, request
import pandas as pd
from scraper import scrape_argos, scrape_pcworld, scrape_ebay

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    query = ""
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        
        argos = scrape_argos(query)
        pcworld = scrape_pcworld(query)
        ebay = scrape_ebay(query)
        
        all_products = argos + pcworld + ebay
        if all_products:
            df = pd.DataFrame(all_products)
            df = df.sort_values(by="price", ascending=True)
            results = df.to_html(classes='table table-striped', index=False, escape=False)
    
    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)