from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates')

@app.route("/")
def index():
    html = """
    <h2>🔫 DealPrism - Working ✅</h2>
    <p>Argos Top Deals • Profit Finder</p>
    <p><strong>Basic version is live.</strong></p>
    <p>Full scraping + profit calculator coming tomorrow when we're fresh.</p>
    """
    return render_template("index.html", results=html)

if __name__ == "__main__":
    app.run(debug=True)
