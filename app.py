"""
This module runs the Flask web application for the Astra Export Parser.
"""

from flask import Flask, render_template, request

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
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        product_names_full = list(astra_parser.get_product_names(astra_parser.FILENAME))
        total = len(product_names_full)
        start = (page - 1) * per_page
        end = start + per_page
        product_names = product_names_full[start:end]
        total_pages = (total + per_page - 1) // per_page
    except (FileNotFoundError, ValueError) as e:
        return f"Error: {e}", 500
    return render_template(
        "index.html",
        result_type="names",
        data=product_names,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages
    )


@app.route("/parts")
def parts():
    """Displays the list of spare parts."""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        spare_parts_full = list(astra_parser.get_spare_parts(astra_parser.FILENAME))
        total = len(spare_parts_full)
        start = (page - 1) * per_page
        end = start + per_page
        spare_parts = spare_parts_full[start:end]
        total_pages = (total + per_page - 1) // per_page
    except (FileNotFoundError, ValueError) as e:
        return f"Error: {e}", 500
    return render_template(
        "index.html",
        result_type="parts",
        data=dict(spare_parts),
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
