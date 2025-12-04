"""
This module runs the Flask web application for the Astra Export Parser.
"""

from flask import Flask, render_template

import astra_parser

app = Flask(__name__)

# Load the XML root once when the app starts
try:
    ROOT = astra_parser.load_xml(astra_parser.FILENAME)
except (FileNotFoundError, ValueError) as e:
    print(f"Error loading XML: {e}")
    ROOT = None


@app.route("/")
def index():
    """Renders the main index page."""
    return render_template("index.html")


@app.route("/count")
def count():
    """Displays the total count of products."""
    if ROOT is None:
        return "Error: XML file not loaded.", 500
    product_count = astra_parser.count_products(ROOT)
    return render_template("index.html", result_type="count", data=product_count)


@app.route("/names")
def names():
    """Displays the list of product names."""
    if ROOT is None:
        return "Error: XML file not loaded.", 500
    product_names = astra_parser.get_product_names(ROOT)
    return render_template("index.html", result_type="names", data=product_names)


@app.route("/parts")
def parts():
    """Displays the list of spare parts."""
    if ROOT is None:
        return "Error: XML file not loaded.", 500
    spare_parts = astra_parser.get_spare_parts(ROOT)
    return render_template("index.html", result_type="parts", data=dict(spare_parts))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
