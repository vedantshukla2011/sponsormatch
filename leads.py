import googlemaps

def fetch_leads(location, keyword, api_key):
    gmaps = googlemaps.Client(key=api_key)
    
    # Geocode the input location string
    geocode_result = gmaps.geocode(location)
    if not geocode_result:
        raise Exception(f"Could not geocode location: {location}")
        
    lat_lng = geocode_result[0]["geometry"]["location"]
    
    # Fetch nearby places matching keyword
    places_result = gmaps.places(query=keyword, location=lat_lng, radius=15000)
    
    leads = []
    for place in places_result.get("results", []):
        leads.append({
            "name": place.get("name", "Unknown Business"),
            "address": place.get("formatted_address", "Address unavailable"),
            "rating": place.get("rating", "N/A"),
            "user_ratings_total": place.get("user_ratings_total", 0),
            "types": place.get("types", [])
        })
        
    return leads