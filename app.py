"""
This module runs the Flask web application for the Astra Export Parser.
"""

from flask import Flask, render_template

import astra_parser

app = Flask(__name__)


@app.route("/")
def index():
    """Renders the main index page."""
    return render_template("index.html")


@app.route("/count")
def count():
    """Displays the total count of products."""
    try:
        product_count = astra_parser.count_products(astra_parser.FILENAME)
    except (FileNotFoundError, ValueError) as e:
        return f"Error: {e}", 500
    return render_template("index.html", result_type="count", data=product_count)


@app.route("/names")
def names():
    """Displays the list of product names."""
    try:
        product_names = list(astra_parser.get_product_names(astra_parser.FILENAME))
    except (FileNotFoundError, ValueError) as e:
        return f"Error: {e}", 500
    return render_template("index.html", result_type="names", data=product_names)


@app.route("/parts")
def parts():
    """Displays the list of spare parts."""
    try:
        spare_parts = list(astra_parser.get_spare_parts(astra_parser.FILENAME))
    except (FileNotFoundError, ValueError) as e:
        return f"Error: {e}", 500
    return render_template("index.html", result_type="parts", data=dict(spare_parts))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
