from flask import Flask, jsonify, request
from data import inventory

app = Flask(__name__)


def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def next_id():
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


@app.route("/")
def home():
    return "<h3>Welcome to the inventory management system</h3>"


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    else:
        return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json(silent=True)
    if not data or "product" not in data or "price" not in data:
        return jsonify({"error": "Invalid input"}), 400

    product = data["product"]
    if not isinstance(product, dict) or not product.get("product_name"):
        return jsonify({"error": "Product information is needed"}), 400

    price = data["price"]
    stock = data.get("stock", 0)
    if not isinstance(price, (int, float)) or price < 0:
        return jsonify({"error": "Price must be a number, 0 or higher"}), 400
    if not isinstance(stock, int) or stock < 0:
        return jsonify({"error": "Stock must be a whole number, 0 or higher"}), 400

    new_item = {
        "id": next_id(),
        "status": 1,
        "barcode": data.get("barcode", ""),
        "price": price,
        "stock": stock,
        "product": {
            "product_name": product["product_name"],
            "brands": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", ""),
        },
    }
    inventory.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)
