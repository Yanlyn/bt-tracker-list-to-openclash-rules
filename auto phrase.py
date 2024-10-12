import requests
from urllib.parse import urlparse

# URLs of the raw BT tracker lists
tracker_list_urls = [
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_ws.txt"
    "https://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt"
    "https://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all_ws.txt"
]

# Output file where the Clash rules will be written (now ending with .list)
output_file = "clash_bt_trackers.list"

def get_domain_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

def generate_clash_rules(trackers):
    clash_rules = set()  # Use a set to avoid duplicates
    for tracker in trackers:
        domain = get_domain_from_url(tracker)
        if domain:
            # Use DOMAIN[] for exact domain match
            clash_rules.add(f"DOMAIN,{domain}")
    return sorted(clash_rules)  # Sort the output for readability

def main():
    all_trackers = []
    for url in tracker_list_urls:
        # Fetch each tracker list
        response = requests.get(url)
        if response.status_code == 200:
            trackers = response.text.strip().split("\n")
            all_trackers.extend(trackers)
        else:
            print(f"Failed to fetch tracker list from {url}. Status code: {response.status_code}")
    
    # Generate Clash rules
    clash_rules = generate_clash_rules(all_trackers)

    # Write rules to the output file (with .list extension)
    with open(output_file, "w") as f:
        f.write("\n".join(clash_rules))
    print(f"Clash rules generated and saved to {output_file}")

if __name__ == "__main__":
    main()
