from geopy.geocoders import Nominatim
import requests
import time

from database.donations import fulfill_pending_orders

geolocator = Nominatim(user_agent="mealmatch-mapping-demo")


def geocode(address: str):
    location = geolocator.geocode(address)
    if not location:
        return None
    return location.latitude, location.longitude


def get_route(start_lat, start_lon, end_lat, end_lon):
    url = (
        "http://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
        "?overview=false"
    )
t
    response = requests.get(url, timeout=15)
    data = response.json()

    if data.get("code") != "Ok":
        return None

    route = data["routes"][0]
    distance_km = route["distance"] / 1000
    duration_min = route["duration"] / 60

    return distance_km, duration_min


def build_full_address(order: dict) -> str:
    parts = [
        order.get("address_line1"),
        order.get("address_line2"),
        order.get("city"),
        order.get("state"),
        order.get("postal_code"),
    ]
    return ", ".join(part for part in parts if part)


def map_orders(start_address: str):
    # WARNING:
    # fulfill_pending_orders() marks orders as completed.
    # If you only want to preview routes, use list_pending_orders() instead.
    orders = fulfill_pending_orders()

    if not orders:
        print("No pending orders found.")
        return

    start_coords = geocode(start_address)
    if not start_coords:
        print("Could not geocode the starting address.")
        return

    start_lat, start_lon = start_coords
    results = []

    for order in orders:
        full_address = build_full_address(order)
        coords = geocode(full_address)
        time.sleep(1)  # be polite to Nominatim

        if not coords:
            print(f"Could not geocode: {full_address}")
            continue

        end_lat, end_lon = coords
        route = get_route(start_lat, start_lon, end_lat, end_lon)

        if not route:
            print(f"Could not route to: {full_address}")
            continue

        distance_km, duration_min = route
        results.append({
            "donation_id": order["donation_id"],
            "account_name": order["account_name"],
            "address": full_address,
            "distance_km": distance_km,
            "duration_min": duration_min,
        })

    results.sort(key=lambda x: x["distance_km"])

    print("\n=== Routes to Donation Addresses ===\n")
    for i, r in enumerate(results, start=1):
        print(f"{i}. Donation #{r['donation_id']} for {r['account_name']}")
        print(f"   Address: {r['address']}")
        print(f"   Distance: {r['distance_km']:.2f} km")
        print(f"   Drive Time: {r['duration_min']:.0f} minutes\n")


def main():
    start_address = input("Enter the starting location: ").strip()
    map_orders(start_address)


if __name__ == "__main__":
    main()

