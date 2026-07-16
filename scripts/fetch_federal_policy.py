import json
import os
from datetime import datetime, timedelta
import requests

# Define absolute file paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))
classified_file_path = os.path.join(data_dir, "classified_organizations.json")
policy_output_path = os.path.join(data_dir, "weekly_policy_updates.json")

# Ensure target directory exists
os.makedirs(data_dir, exist_ok=True)

# Agency mapping matching the Federal Register slugs
# Updated Agency slugs matching the official Federal Register Registry
FEDERAL_AGENCY_MAPPING = {
    "healthcare_behavioral_disability": [
        "health-and-human-services-department",
        "substance-abuse-and-mental-health-services-administration",
        "health-resources-and-services-administration",
        "centers-for-medicare-medicaid-services",
        "community-living-administration",  # Corrected from administration-for-community-living
        "centers-for-disease-control-and-prevention",
        "food-and-drug-administration",
        "national-institutes-of-health"
    ],
    "child_welfare_housing": [
        "children-and-families-administration",
        "housing-and-urban-development-department"  # Handles Community Planning & Development Office
    ],
    "education_youth_development": [
        "education-department"  # Handles Special Ed, Elementary, and Postsecondary Offices
    ],
    "food_security_basic_needs": [
        "agriculture-department",
        "food-and-nutrition-service",
        "federal-emergency-management-agency"
    ],
    "community_advocacy_workforce": [
        "labor-department",
        "employment-and-training-administration",
        "u-s-citizenship-and-immigration-services",
        "civil-rights-commission",
        "equal-employment-opportunity-commission"
    ],
    "arts_culture_preservation": [
        "national-foundation-on-the-arts-and-the-humanities",
        "national-endowment-for-the-arts",
        "national-endowment-for-the-humanities",
        "institute-of-museum-and-library-services",
        "national-park-service",
        "advisory-council-on-historic-preservation"
    ]
}

def fetch_federal_updates_for_domain(domain_key, agency_slugs, days_back=7):
    """
    Queries the Federal Register API and automatically paginates through 
    the next_page_url keys to retrieve all matching documents from the last N days.
    """
    date_threshold = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    # Prepare initial request parameters
    url = "https://www.federalregister.gov/api/v1/documents.json"
    params = {
        "conditions[type][]": ["RULE", "PRORULE", "NOTICE"],
        "conditions[publication_date][gte]": date_threshold,
        "per_page": 100,  # Maximize the page size to reduce API calls
        "order": "newest",
        # Pass the list directly to let requests format the repeated query keys correctly
        "conditions[agencies][]": agency_slugs
    }
    
    parsed_updates = []
    page_count = 1

    try:
        while url:
            # On page 1, pass the structured params. For subsequent pages, requests uses the next_page_url directly.
            response = requests.get(url, params=params if page_count == 1 else None, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            raw_documents = data.get("results", [])
            for doc in raw_documents:
                parsed_updates.append({
                    "title": doc.get("title"),
                    "type": doc.get("type"),
                    "publication_date": doc.get("publication_date"),
                    "agencies": [agency.get("name") for agency in doc.get("agencies", [])],
                    "abstract": doc.get("abstract") or doc.get("action", "No summary abstract provided."),
                    "document_url": doc.get("html_url"),
                    "pdf_url": doc.get("pdf_url"),
                    "document_number": doc.get("document_number"),
                    "action_type": doc.get("action")
                })
            
            # Check for next page
            url = data.get("next_page_url")
            if url:
                page_count += 1
                
        return parsed_updates

    except Exception as e:
        print(f"   [API Fetch Fail] Failed to retrieve data on page {page_count} for {domain_key}: {e}")
        return parsed_updates


def run_policy_fetcher():
    print("Initializing Stage 2/3: Fetching Federal Policy Updates...")
    
    if not os.path.exists(classified_file_path):
        print(f"Warning: Classified dataset not found at '{classified_file_path}'. Utilizing schema boundaries directly.")
        
    weekly_digest = {
        "metadata": {
            "fetched_at": datetime.now().isoformat(),
            "coverage_days": 7
        },
        "updates": {}
    }
    
    total_found = 0
    
    for domain_key, agency_slugs in FEDERAL_AGENCY_MAPPING.items():
        print(f"-> Fetching federal updates for: {domain_key}...")
        updates = fetch_federal_updates_for_domain(domain_key, agency_slugs)
        
        weekly_digest["updates"][domain_key] = updates
        total_found += len(updates)
        print(f"   Success! Collected {len(updates)} total updates for this domain.")
        
    # Write output to our project's data folder
    with open(policy_output_path, "w", encoding="utf-8") as f:
        json.dump(weekly_digest, f, indent=4, ensure_ascii=False)
        
    print(f"\nSuccessfully completed Federal Policy tracking with pagination!")
    print(f"Fetched a grand total of {total_found} recent updates across all domains.")
    print(f"Saved paginated policy feed directly to: {policy_output_path}")


if __name__ == "__main__":
    run_policy_fetcher()