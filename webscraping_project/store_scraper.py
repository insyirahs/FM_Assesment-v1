import requests
import pandas as pd

def get_places(query, brand):
    url = "https://overpass.kumi.systems/api/interpreter"

    overpass_query = f"""
    [out:json][timeout:60];
    node
      ["name"~"{query}", i]
      (3.0,101.0,7.5,119.0);
    out center;
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(
        url,
        data=overpass_query,
        headers=headers,
        timeout=90
    )

    print(f"\nSTATUS for {brand}:", response.status_code)
    print(response.text[:200])

    try:
        data = response.json()
    except:
        print("❌ API failed")
        return []

    results = []

    for element in data.get("elements", []):
        lat = element.get("lat")
        lon = element.get("lon")
        name = element.get("tags", {}).get("name", "Unknown")

        results.append({
            "Brand": brand,
            "Store Name": name,
            "Latitude": lat,
            "Longitude": lon,
            "Address": ""
        })

    return results
