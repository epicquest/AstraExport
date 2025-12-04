"""
This module parses the Astra Export XML file and provides functions to extract
product information such as counts, names, and spare parts.
"""

import xml.etree.ElementTree as ET

FILENAME = "data/export_full.xml"


def count_products(filename):
    """Counts the total number of products (items) in the file using streaming parse."""
    count = 0
    path = []
    for event, elem in ET.iterparse(filename, events=("start", "end")):
        if event == "start":
            path.append(elem.tag)
        elif event == "end":
            if elem.tag == "item" and len(path) >= 2 and path[-2] == "items":
                count += 1
            path.pop()
            if elem.tag == "item" and path and path[-1] == "items":
                elem.clear()
    return count


def get_product_names(filename, start=0, limit=None):
    """Yields product name and image dicts using streaming parse."""
    path = []
    count = 0
    for event, elem in ET.iterparse(filename, events=("start", "end")):
        if event == "start":
            path.append(elem.tag)
        elif event == "end":
            if elem.tag == "item" and len(path) >= 2 and path[-2] == "items":
                if count >= start and (limit is None or count < start + limit):
                    name = elem.get("name")
                    image = elem.get("image")
                    if name:
                        yield {"name": name, "image": image}
                count += 1
                if limit is not None and count >= start + limit:
                    break
            path.pop()
            if elem.tag == "item" and path and path[-1] == "items":
                elem.clear()


def count_spare_parts(filename):
    """Counts the total number of products with spare parts using streaming parse."""
    count = 0
    path = []
    for event, elem in ET.iterparse(filename, events=("start", "end")):
        if event == "start":
            path.append(elem.tag)
        elif event == "end":
            if elem.tag == "item" and len(path) >= 2 and path[-2] == "items":
                parts_container = elem.find("parts")
                if parts_container is not None:
                    spare_parts = _extract_parts(parts_container)
                    if spare_parts:
                        count += 1
            path.pop()
            if elem.tag == "item" and path and path[-1] == "items":
                elem.clear()
    return count


def _extract_parts(parts_container):
    """Extracts list of part names from a parts container element."""
    parts = []
    for part in parts_container:
        if part.tag == "part":
            item = part.find("item")
            if item is not None:
                part_name = item.get("name")
                if part_name:
                    parts.append(part_name)
    return parts


def get_spare_parts(filename, start=0, limit=None):
    """Yields (product_name, details) tuples for products with spare parts."""
    path = []
    count = 0
    for event, elem in ET.iterparse(filename, events=("start", "end")):
        if event == "start":
            path.append(elem.tag)
        elif event == "end":
            if elem.tag == "item" and len(path) >= 2 and path[-2] == "items":
                parts_container = elem.find("parts")
                if parts_container is None:
                    path.pop()
                    if elem.tag == "item" and path and path[-1] == "items":
                        elem.clear()
                    continue
                spare_parts = _extract_parts(parts_container)
                if not spare_parts:
                    path.pop()
                    if elem.tag == "item" and path and path[-1] == "items":
                        elem.clear()
                    continue
                if count >= start and (limit is None or count < start + limit):
                    product_name = elem.get("name") or "Unknown Product"
                    image = elem.get("image")
                    yield (product_name, {"parts": spare_parts, "image": image})
                count += 1
                if limit is not None and count >= start + limit:
                    break
            path.pop()
            if elem.tag == "item" and path and path[-1] == "items":
                elem.clear()


def main_menu():
    """Displays the main menu and returns the user's choice."""
    print("\n--- Astra Export Parser Menu ---")
    print("1. Count total products")
    print("2. Print all product names")
    print("3. List spare parts")
    print("q. Quit")
    choice = input("Enter your choice (1, 2, 3, or q): ")
    return choice


def run_app():
    """Runs the main application loop."""
    while True:
        choice = main_menu()
        if choice == "1":
            count = count_products(FILENAME)
            print(f"Total products: {count}")
        elif choice == "2":
            print("Product Names:")
            products = get_product_names(FILENAME)
            for product in products:
                print(product["name"])
        elif choice == "3":
            print("Spare Parts:")
            parts_data = get_spare_parts(FILENAME)
            for product, details in parts_data:
                print(f"{product}: {details['parts']}")
        elif choice.lower() == "q":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_app()
