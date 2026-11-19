# Flask Inventory Management System

A small REST API built with Flask that manages a product inventory, with a
command-line interface. Product details can be fetched from the
OpenFoodFacts API. Prices are in Kenya Shillings (KES).

## Files

- `app.py` - Flask routes
- `data.py` - mock inventory (a Python list, resets when the server restarts)
- `openfoodfacts.py` - OpenFoodFacts API client
- `cli.py` - command-line interface
- `requirements.txt` - Python dependencies

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Start the server in one terminal:

```
python app.py
```

Start the CLI in a second terminal (with the virtual environment active):

```
python cli.py
```

## Routes

- `GET /inventory` - returns all items (200)
- `GET /inventory/<id>` - returns one item (200), or 404
- `POST /inventory` - adds an item (201). Send JSON with `price`, optional
  `stock`, and either a `barcode` or a `product` with a `product_name`.
  Returns 400 for invalid input, or 502 if OpenFoodFacts is unreachable
- `PATCH /inventory/<id>` - updates price, stock or product details (200),
  or 400 / 404
- `DELETE /inventory/<id>` - removes an item (200), or 404
- `GET /search?barcode=...` or `GET /search?name=...` - looks a product up on
  OpenFoodFacts without changing the inventory (200), or 404 / 400 / 502

If POST receives a barcode, the product name, brand and ingredients are
fetched from OpenFoodFacts. If the barcode is not found there, the product
details you sent are used instead.

## Item format

```
{
  "id": 1,
  "status": 1,
  "barcode": "61600101",
  "price": 65.0,
  "stock": 120,
  "product": {
    "product_name": "Fresh Milk 500ml",
    "brands": "Brookside",
    "ingredients_text": "Pasteurised whole milk"
  }
}
```

## CLI menu

1. View all items
2. View one item
3. Add an item (by barcode or by hand)
4. Update price or stock
5. Delete an item
6. Find a product on OpenFoodFacts and add it to the inventory
0. Quit

To try the OpenFoodFacts lookup, add an item with the barcode `6111246721278` or .

The CLI prints "Server unreachable." if the server is not running.