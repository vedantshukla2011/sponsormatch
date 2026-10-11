import requests

def fetch_leads(location, keyword, api_key):
    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.types"
    }
    
    query_str = f"{keyword} in {location}" if location else keyword
    
    payload = {
        "textQuery": query_str,
        "pageSize": 20
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"API Error ({response.status_code}): {response.text}")
        
    data = response.json()
    places = data.get("places", [])
    
    leads = []
    for place in places:
        display_name = place.get("displayName", {}).get("text", "Unknown Business")
        leads.append({
            "name": display_name,
            "address": place.get("formattedAddress", "Address unavailable"),
            "rating": place.get("rating", "N/A"),
            "user_ratings_total": place.get("userRatingCount", 0),
            "types": place.get("types", [])
        })
        
    return leads