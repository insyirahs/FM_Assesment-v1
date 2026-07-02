import requests
import pandas as pd
import time

API_KEY = "YOUR_GOOGLE_PLACES_API_KEY"

brands = [
    "99 Speedmart Malaysia",
    "7-Eleven Malaysia",
    "CU Mart Malaysia"
]

regions = [
    ("Kuala Lumpur", 3.1390, 101.6869),
    ("Selangor", 3.0738, 101.5183),
    ("Penang", 5.4164, 100.3327),
    ("Johor Bahru", 1.4927, 103.7414),
    ("Ipoh", 4.5975, 101.0901),
    ("Melaka", 2.1896, 102.2501),
    ("Kota Kinabalu", 5.9804, 116.0735),
    ("Kuching", 1.5533, 110.3592)
]

results = []

for brand in brands:
    for region_name, lat, lng in regions:

        print(f"\nSearching {brand} in {region_name}")

        url = "https://places.googleapis.com/v1/places:searchText"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location"
        }

        body = {
            "textQuery": brand,
            "locationBias": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lng
                    },
                    "radius": 50000
                }
            }
        }

        response = requests.post(url, json=body, headers=headers)
        data = response.json()

        places = data.get("places", [])

        print("Results found:", len(places))

        for place in places:
            location = place.get("location", {})

            results.append({
                "Brand": brand,
                "Store Name": place.get("displayName", {}).get("text"),
                "Latitude": location.get("latitude"),
                "Longitude": location.get("longitude"),
                "Address": place.get("formattedAddress"),
                "Region": region_name
            })

        time.sleep(0.2)

print("\nTOTAL RESULTS:", len(results))

if len(results) == 0:
    print("No data collected. Check API key or requests.")
    exit()

df = pd.DataFrame(results)

print("\nColumns:", df.columns)

df = df.drop_duplicates(subset=["Store Name", "Address"])
df = df.sort_values(by=["Brand", "Store Name"]).reset_index(drop=True)
df.to_csv("store_locations.csv", index=False)

print("\nDONE! dataset created.")
print("Total stores:", len(df))
print("\nStore count by brand:")
print(df["Brand"].value_counts())