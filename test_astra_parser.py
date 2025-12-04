"""
Unit tests for the Astra Parser module.
"""

import os
import tempfile
import unittest

import astra_parser as parser_module
from app import app as flask_app
from astra_parser import count_products, get_product_names, get_spare_parts


class TestAstraParser(unittest.TestCase):
    """Test cases for Astra Parser functions."""

    def setUp(self):
        """Set up a sample XML structure for testing."""
        self.xml_string = """
        <export>
          <items>
            <item name="Test Product 1">
              <parts>
                <part>
                   <item name="Part A" />
                </part>
              </parts>
            </item>
            <item name="Test Product 2">
            </item>
          </items>
        </export>
        """
        self.xml_string = self.xml_string.strip()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
            f.write(self.xml_string)
            self.filename = f.name

    def tearDown(self):
        """Clean up the temporary file."""
        os.unlink(self.filename)

    def test_count_products(self):
        """Test that the product count is correct."""
        self.assertEqual(count_products(self.filename), 2)

    def test_product_names(self):
        """Test that product names are extracted correctly."""
        products = get_product_names(self.filename)
        names = [p["name"] for p in products]
        self.assertIn("Test Product 1", names)
        self.assertIn("Test Product 2", names)

    def test_spare_parts(self):
        """Test that spare parts are extracted correctly."""
        parts_data = dict(get_spare_parts(self.filename))
        self.assertIn("Test Product 1", parts_data)
        self.assertEqual(parts_data["Test Product 1"]["parts"], ["Part A"])

    def test_get_product_names_limit(self):
        """Test that get_product_names respects the `limit` argument.

        The function should yield only the requested number of items.
        """
        # Build a temporary XML with many items
        item_list = [f'<item name="Product {i}" />' for i in range(1, 51)]
        many_items_xml = "<export><items>" + "".join(item_list) + "</items></export>"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
            f.write(many_items_xml)
            many_filename = f.name
        try:
            products = list(get_product_names(many_filename, start=0, limit=10))
            self.assertEqual(len(products), 10)
            self.assertEqual(products[0]["name"], "Product 1")
        finally:
            os.unlink(many_filename)

    def test_names_endpoint_does_not_compute_total(self):
        """Test the Flask `/names` endpoint returns page info without the total count.

        We monkey-patch the parser module's FILENAME to point to our temporary file and
        verify HTML doesn't contain the total items text.
        """
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
            # create simple XML with 3 items
            f.write(self.xml_string)
            afilename = f.name
        # patch the astra_parser.FILENAME used by app
        parser_module.FILENAME = afilename
        client = flask_app.test_client()
        resp = client.get("/names")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("Page 1", html)
        self.assertNotIn("total items", html)
        os.unlink(afilename)

    def test_names_endpoint_next_link_shows_if_more(self):
        """When the number of items equals `per_page`, the endpoint should
        show a Next link.

        This indicates there may be a subsequent page. We check that the 'Next' text
        appears in the paginated HTML response.
        """
        # Create an XML with 20 items and set the parser FILENAME to it
        item_list = [f'<item name="Product {i}" />' for i in range(1, 21)]
        many_items_xml = "<export><items>" + "".join(item_list) + "</items></export>"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
            f.write(many_items_xml)
            many_filename = f.name
        parser_module.FILENAME = many_filename
        client = flask_app.test_client()
        resp = client.get("/names")
        html = resp.get_data(as_text=True)
        # default per_page is 10, so there should be a Next link
        self.assertIn("Next", html)
        os.unlink(many_filename)


if __name__ == "__main__":
    unittest.main()
