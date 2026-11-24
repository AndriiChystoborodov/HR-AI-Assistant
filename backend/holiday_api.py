"""
OpenHolidays API client for Swiss/Cantonal holiday data.
Fetches holidays and cleans/normalizes the JSON response.
"""

import requests
from datetime import date


BASE_URL = "https://openholidaysapi.org"


def fetch_holidays(
    country_iso: str = "CH",
    language_iso: str = "EN",
    valid_from: str = None,
    valid_to: str = None,
    subdivision_code: str = "CH-BS",
) -> list[dict]:
    """
    Fetch public holidays from the OpenHolidays API.

    Args:
        country_iso: ISO 3166-1 alpha-2 country code (default: 'CH' for Switzerland).
        language_iso: ISO 639-1 language code for holiday names (default: 'EN').
        valid_from: Start date in YYYY-MM-DD format (default: current year Jan 1).
        valid_to: End date in YYYY-MM-DD format (default: current year Dec 31).
        subdivision_code: Canton code, e.g. 'CH-ZH' for Zurich (optional).

    Returns:
        List of cleaned holiday dicts.
    """
    year = date.today().year
    valid_from = valid_from or f"{year}-01-01"
    valid_to = valid_to or f"{year}-12-31"

    params = {
        "countryIsoCode": country_iso,
        "languageIsoCode": language_iso,
        "validFrom": valid_from,
        "validTo": valid_to,
    }
    if subdivision_code:
        params["subdivisionCode"] = subdivision_code

    url = f"{BASE_URL}/PublicHolidays"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    raw = response.json()
    return clean_holidays(raw)


def clean_holidays(raw: list[dict]) -> list[dict]:
    """
    Clean and normalize raw holiday records from the API response.

    Keeps only relevant fields and flattens nested name/comment lists
    into a single string for the requested language.

    Args:
        raw: Raw list of holiday objects from the API.

    Returns:
        List of cleaned holiday dicts with keys:
            - id, name, start_date, end_date, type, nationwide, subdivisions
    """
    cleaned = []
    for item in raw:
        name = _extract_first_text(item.get("name", []))
        cleaned.append(
            {
                "id": item.get("id", ""),
                "name": name,
                "start_date": item.get("startDate", ""),
                "end_date": item.get("endDate", ""),
                "type": item.get("type", ""),
                "nationwide": item.get("nationwide", False),
                "subdivisions": _extract_subdivision_codes(
                    item.get("subdivisions", [])
                ),
            }
        )
    return cleaned


def _extract_first_text(name_list: list[dict]) -> str:
    """Return the first text value from a [{language, text}] list."""
    if not name_list:
        return ""
    return name_list[0].get("text", "")


def _extract_subdivision_codes(subdivisions: list[dict]) -> list[str]:
    """Extract short codes from subdivision objects."""
    return [s.get("code", "") for s in subdivisions if s.get("code")]


def display_holidays(holidays: list[dict]) -> None:
    """Print holidays in a readable table format."""
    if not holidays:
        print("No holidays found.")
        return

    print(f"{'Date':<12} {'Name':<40} {'Type':<20} {'Nationwide'}")
    print("-" * 85)
    for h in holidays:
        date_str = h["start_date"]
        name = h["name"][:38]
        htype = h["type"][:18]
        nationwide = "Yes" if h["nationwide"] else "No"
        print(f"{date_str:<12} {name:<40} {htype:<20} {nationwide}")


if __name__ == "__main__":
    # Fetch Basel-Stadt (CH-BS) cantonal holidays for the current year
    print("Fetching Basel-Stadt (CH-BS) holidays...\n")
    holidays = fetch_holidays(
        country_iso="CH",
        language_iso="EN",
        subdivision_code="CH-BS",
    )
    display_holidays(holidays)
