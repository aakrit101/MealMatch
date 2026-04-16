import os
import sys
import time
from typing import List, Dict, Any, Optional, Tuple

import requests
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(ENV_PATH, override=True)
sys.path.append(PROJECT_ROOT)

from database.donations import list_pending_orders
from database.accounts import list_accounts

geolocator = Nominatim(user_agent="mealmatch-route-optimizer")


def geocode(address: str) -> Optional[Tuple[float, float]]:
    location = geolocator.geocode(address)
    if not location:
        return None
    return (location.latitude, location.longitude)


def get_route(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Optional[Tuple[float, float]]:
    url = (
        "http://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
        "?overview=false"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return None

    if data.get("code") != "Ok" or not data.get("routes"):
        return None

    route = data["routes"][0]
    distance_km = route["distance"] / 1000
    duration_min = route["duration"] / 60
    return (distance_km, duration_min)


def build_full_address(row: Dict[str, Any]) -> str:
    parts = [
        row.get("address_line1"),
        row.get("address_line2"),
        row.get("city"),
        row.get("state"),
        row.get("postal_code"),
    ]
    return ", ".join(part for part in parts if part)


def _prepare_stops(rows: List[Dict[str, Any]], source_type: str) -> List[Dict[str, Any]]:
    stops: List[Dict[str, Any]] = []

    for row in rows:
        address = build_full_address(row)
        coords = geocode(address)
        time.sleep(1)

        if not coords:
            print(f"Skipping ungeocodable address: {address}")
            continue

        stop: Dict[str, Any] = {
            "source_type": source_type,
            "account_name": row.get("account_name"),
            "address": address,
            "latitude": coords[0],
            "longitude": coords[1],
        }

        if source_type == "pending":
            stop["donation_id"] = row.get("donation_id")
            stop["notes"] = row.get("notes")
            stop["donated_at"] = row.get("donated_at")
            stop["status"] = row.get("status")
        else:
            stop["account_id"] = row.get("id")
            stop["created_at"] = row.get("created_at")
            stop["food_genre"] = row.get("food_genre")

        stops.append(stop)

    return stops


def _nearest_neighbor_route(start_address: str, stops: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    start_coords = geocode(start_address)
    if not start_coords:
        raise ValueError("Could not geocode the starting address.")

    remaining = stops[:]
    ordered: List[Dict[str, Any]] = []

    current_lat, current_lon = start_coords
    stop_number = 1
    total_distance_km = 0.0
    total_duration_min = 0.0

    while remaining:
        best_idx = None
        best_route = None

        for idx, stop in enumerate(remaining):
            route = get_route(current_lat, current_lon, stop["latitude"], stop["longitude"])
            if route is None:
                continue

            if best_route is None or route[0] < best_route[0]:
                best_idx = idx
                best_route = route

        if best_idx is None or best_route is None:
            print("Some remaining stops could not be routed and were skipped.")
            break

        chosen = remaining.pop(best_idx)
        leg_distance_km, leg_duration_min = best_route

        total_distance_km += leg_distance_km
        total_duration_min += leg_duration_min

        chosen["stop_number"] = stop_number
        chosen["leg_distance_km"] = round(leg_distance_km, 2)
        chosen["leg_duration_min"] = round(leg_duration_min, 1)
        chosen["running_total_distance_km"] = round(total_distance_km, 2)
        chosen["running_total_duration_min"] = round(total_duration_min, 1)

        ordered.append(chosen)

        current_lat = chosen["latitude"]
        current_lon = chosen["longitude"]
        stop_number += 1

    return ordered


def optimize_pending_pickup_order(start_address: str) -> List[Dict[str, Any]]:
    rows = list_pending_orders()
    if not rows:
        return []
    return _nearest_neighbor_route(start_address, _prepare_stops(rows, "pending"))


def optimize_all_accounts_pickup_order(start_address: str) -> List[Dict[str, Any]]:
    rows = list_accounts()
    if not rows:
        return []
    return _nearest_neighbor_route(start_address, _prepare_stops(rows, "accounts"))


def print_route(route: List[Dict[str, Any]], title: str) -> None:
    print(f"\n=== {title} ===\n")

    if not route:
        print("No stops found.\n")
        return

    for stop in route:
        print(f"Stop {stop['stop_number']}: {stop.get('account_name', 'Unknown')}")
        print(f"  Address: {stop['address']}")
        print(f"  Leg Distance: {stop['leg_distance_km']:.2f} km")
        print(f"  Leg Time: {stop['leg_duration_min']:.1f} min")
        print(f"  Running Total Distance: {stop['running_total_distance_km']:.2f} km")
        print(f"  Running Total Time: {stop['running_total_duration_min']:.1f} min")
        print()


def main() -> None:
    print("1. Optimize pending pickup order")
    print("2. Optimize all accounts pickup order (test mode)")
    choice = input("Choose an option (1 or 2): ").strip()
    start_address = input("Enter the starting location: ").strip()

    if choice == "1":
        route = optimize_pending_pickup_order(start_address)
        print_route(route, "Optimized Pending Pickup Order")
    elif choice == "2":
        route = optimize_all_accounts_pickup_order(start_address)
        print_route(route, "Optimized All-Accounts Pickup Order")
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
