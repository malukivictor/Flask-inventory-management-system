import requests

api_url = "http://127.0.0.1:5000"

def show(item):
    product = item["product"]
    print(item["id"], product["product_name"], product["brands"],
          "| KES", item["price"], "| stock", item["stock"])

def view_all():
    try:
        response = requests.get(api_url + "/inventory", timeout=15)
        for item in response.json():
            show(item)
    except requests.RequestException:
        print("Server is unreachable.")

def view_one():
    try:
        item_id = int(input("Item ID: "))
        response = requests.get(api_url + "/inventory/" + str(item_id), timeout=15)
        if response.ok:
            show(response.json())
        else:
            print(response.json()["error"])
    except ValueError:
        print("Enter a whole number.")
    except requests.RequestException:
        print("Server unreachable.")

def add_item():
    try:
        barcode = input("Barcode: ").strip()
        body = {}
        if barcode:
            body["barcode"] = barcode
        else:
            body["product"] = {
                "product_name": input("Name: ").strip(),
                "brands": input("Brand: ").strip(),
            }
        body["price"] = float(input("Price (KES): "))
        body["stock"] = int(input("Stock: "))

        response = requests.post(api_url + "/inventory", json=body, timeout=15)
        if response.ok:
            show(response.json())
        else:
            print(response.json()["error"])
    except ValueError:
        print("Enter valid numbers.")
    except requests.RequestException:
        print("Server unreachable.")

def update_item():
    try:
        item_id = int(input("Item ID: "))
        price = input("New price (blank to skip): ").strip()
        stock = input("New stock (blank to skip): ").strip()
        body = {}
        if price:
            body["price"] = float(price)
        if stock:
            body["stock"] = int(stock)

        response = requests.patch(api_url + "/inventory/" + str(item_id), json=body, timeout=15)
        if response.ok:
            show(response.json())
        else:
            print(response.json()["error"])
    except ValueError:
        print("Enter valid numbers.")
    except requests.RequestException:
        print("Server unreachable.")

def delete_item():
    try:
        item_id = int(input("Item ID: "))
        if input("Sure? (yes/no): ") != "yes":
            print("Cancelled.")
            return
        response = requests.delete(api_url + "/inventory/" + str(item_id), timeout=15)
        print(response.json().get("message") or response.json()["error"])
    except ValueError:
        print("Enter a whole number.")
    except requests.RequestException:
        print("Server unreachable.")

def find_on_api():
    try:
        term = input("Search barcode or name: ").strip()
        if term.isdigit():
            response = requests.get(api_url + "/search", params={"barcode": term}, timeout=15)
        else:
            response = requests.get(api_url + "/search", params={"name": term}, timeout=15)

        if not response.ok:
            print(response.json()["error"])
            return

        results = response.json()
        for number, product in enumerate(results, start=1):
            print(number, product["product_name"], product["brands"], "| barcode", product["barcode"])

        choice = int(input("Number to add (0 to skip): "))
        if choice < 1 or choice > len(results):
            return
        body = {
            "barcode": results[choice - 1]["barcode"],
            "price": float(input("Price (KES): ")),
            "stock": int(input("Stock: ")),
        }
        response = requests.post(api_url + "/inventory", json=body, timeout=15)
        if response.ok:
            show(response.json())
        else:
            print(response.json()["error"])
    except ValueError:
        print("Enter valid numbers.")
    except requests.RequestException:
        print("Server unreachable.")

while True:
    print("\n1. View all  2. View one  3. Add  4. Update  5. Delete  6. Find on API  0. Quit")
    choice = input("Choose: ").strip()

    if choice == "1":
        view_all()
    elif choice == "2":
        view_one()
    elif choice == "3":
        add_item()
    elif choice == "4":
        update_item()
    elif choice == "5":
        delete_item()
    elif choice == "6":
        find_on_api()
    elif choice == "0":
        print("kwaheri")
        break
    else:
        print("Invalid choice.")