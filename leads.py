import requests

def get_leads(zip_code, radius_miles, api_key):
    # 1. Geocode Zip Code to Lat/Lng
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={api_key}"
    geo_res = requests.get(geocode_url).json()
    
    if geo_res.get("status") != "OK":
        error_msg = geo_res.get("error_message", geo_res.get("status", "Unknown geocoding error"))
        raise Exception(f"Geocoding API Error: {error_msg}")
        
    location = geo_res["results"][0]["geometry"]["location"]
    
    # 2. Query Places API (New) via REST POST
    places_url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.primaryType"
    }
    payload = {
        "textQuery": "machine shop OR engineering firm OR manufacturing company OR tech company",
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": location["lat"],
                    "longitude": location["lng"]
                },
                "radius": float(radius_miles * 1609.34)  # convert miles to meters
            }
        }
    }
    
    res = requests.post(places_url, json=payload, headers=headers)
    res_data = res.json()
    
    if res.status_code != 200:
        error_details = res_data.get("error", {}).get("message", res.text)
        raise Exception(f"Places API (New) Error ({res.status_code}): {error_details}")
        
    leads = []
    for place in res_data.get("places", []):
        category = place.get("primaryType", "Local Sponsor").replace("_", " ").title()
        leads.append({
            "Name": place.get("displayName", {}).get("text", "N/A"),
            "Address": place.get("formattedAddress", "N/A"),
            "Category": category
        })
    return leads