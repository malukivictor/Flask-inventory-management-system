import requests

base_url = "https://world.openfoodfacts.org"
HEADERS = {
    "User-Agent": "DeathstarMoringa/1.0 (DarthVader)"}
TIMEOUT = 10

class OpenFoodFactsError(Exception):
    pass

def extract_product_fields(product):
    return {
        "product_name": product.get("product_name") or "Unknown",
        "brands": product.get("brands") or "",
        "ingredients_text": product.get("ingredients_text") or "",
    }

def fetch_by_barcode(barcode):
    barcode = str(barcode).strip()
    if not barcode.isdigit():
        return None

    url = f"{base_url}/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as error:
        raise OpenFoodFactsError(
            f"OpenFoodFacts request failed: {error}") from error

    if data.get("status") != 1:
        return None

    return {"barcode": barcode, **extract_product_fields(data["product"])}

def search_by_name(name, limit=5):
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": limit,
    }
    try:
        response = requests.get(
            f"{base_url}/cgi/search.pl",
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as error:
        raise OpenFoodFactsError(
            f"OpenFoodFacts request failed: {error}") from error

    return [
        {"barcode": str(item.get("code", "")), **extract_product_fields(item)}
        for item in data.get("products", [])
    ]



if __name__ == "__main__":
    print(fetch_by_barcode("6111246721278")) 

#OFG barcode for OG cheese 6111246721278
#skimmed milk 6111032009665
#perly 6111242100992