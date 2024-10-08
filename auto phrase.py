import requests
from urllib.parse import urlparse

# URLs of the raw BT tracker lists
tracker_list_urls = [
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_ws.txt"
]

# Output file where the Clash rules will be written
output_file = "clash_bt_trackers.yml"

def get_domain_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

def classify_domain(domain):
    # If the domain has subdomains (more than 2 parts), use DOMAIN-SUFFIX[]
    if domain.count('.') > 1:
        return f"ruleset=🔄 BT Tracker,[]DOMAIN-SUFFIX,{domain}"
    else:
        # Use DOMAIN[] for exact match
        return f"ruleset=🔄 BT Tracker,[]DOMAIN,{domain}"

def generate_clash_rules(trackers):
    clash_rules = set()  # Use a set to automatically handle duplicates
    for tracker in trackers:
        domain = get_domain_from_url(tracker)
        if domain:
            domain_rule = classify_domain(domain)
            clash_rules.add(domain_rule)  # Add rule to set (automatically avoids duplicates)
    return sorted(clash_rules)  # Sort for better readability

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

    # Write rules to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(clash_rules))
    print(f"Clash rules generated and saved to {output_file}")

if __name__ == "__main__":
    main()
