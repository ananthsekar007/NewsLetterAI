import json
import requests
from bs4 import BeautifulSoup
import os


output_dir = "../data"
out_file_path = os.path.join(output_dir, "asu_community_council.json")

# Creating the directory early ensures it exists even if structural parsing changes
os.makedirs(output_dir, exist_ok=True)

def scrape_asu_community_council():
    url = "https://president.asu.edu/the-office/presidents-advisory-councils/community-council"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table containing the council members
    # (Typically contained within the main content block 'table')
    table = soup.find("table")
    if not table:
        print("Could not find the members table on the page.")
        return

    # Find all table rows, excluding the header row if present
    rows = table.find_all("tr")

    council_members = []

    for row in rows:
        # Skip header rows (which usually use <th>)
        if row.find("th"):
            continue

        cols = row.find_all("td")

        # Ensure the row has the expected columns (typically Name in col 1, Position/Org in col 2)
        if len(cols) >= 2:
            # 1. Parse Name
            name_cell = cols[0]
            name = name_cell.get_text(strip=True)

            # If the name itself is linked, capture it
            name_link = name_cell.find("a")
            website = name_link["href"] if name_link else None

            # 2. Parse Position & Organization
            pos_cell = cols[1]

            # Some sites have the website linked in the position/org cell instead
            org_link = pos_cell.find("a")
            if not website and org_link:
                website = org_link["href"]

            # Text formatting: typically split by line breaks or periods
            # We clean it up by replacing multiple spaces/newlines
            details = [
                line.strip()
                for line in pos_cell.stripped_strings
                if line.strip()
            ]

            position = ""
            organization = ""

            if len(details) == 2:
                position = details[0]
                organization = details[1]
            elif len(details) == 1:
                # Fallback if title and organization aren't cleanly split
                position = details[0]
            elif len(details) > 2:
                position = details[0]
                organization = " - ".join(details[1:])

            council_members.append(
                {
                    "name": name,
                    "position": position,
                    "organization": organization,
                    "website": website,
                }
            )

    # Convert the Python list of dicts to a formatted JSON string
    json_output = json.dumps(council_members, indent=4, ensure_ascii=False)

    # Print JSON output to the console
    print(json_output)

    # Save to a local json file
    with open(out_file_path, "w", encoding="utf-8") as f:
        f.write(json_output)


if __name__ == "__main__":
    scrape_asu_community_council()