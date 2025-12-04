"""
Unit tests for the Astra Parser module.
"""

import os
import tempfile
import unittest

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


if __name__ == "__main__":
    unittest.main()
