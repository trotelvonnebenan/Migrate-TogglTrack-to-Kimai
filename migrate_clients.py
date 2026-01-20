import requests
import json
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# --- CONFIGURATION FROM ENV ---
TOGGL_API_TOKEN = os.getenv('TOGGL_API_TOKEN')
TOGGL_WORKSPACE_ID = os.getenv('TOGGL_WORKSPACE_ID')

KIMAI_URL = os.getenv('KIMAI_URL')
KIMAI_API_TOKEN = os.getenv('KIMAI_API_TOKEN')

# Standard Settings (Can also be moved to .env if preferred)
COUNTRY = os.getenv('DEFAULT_COUNTRY', 'AT')
CURRENCY = os.getenv('DEFAULT_CURRENCY', 'EUR')
TIMEZONE = os.getenv('DEFAULT_TIMEZONE', 'Europe/Vienna')

# Headers
toggl_headers = {'Content-Type': 'application/json'}
kimai_headers = {
    'Authorization': f'Bearer {KIMAI_API_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def get_existing_kimai_customers():
    print(f"Connecting to Kimai at {KIMAI_URL}...")
    try:
        response = requests.get(f"{KIMAI_URL}/customers", headers=kimai_headers)
        if response.status_code == 200:
            return {c['name']: c['id'] for c in response.json()}
        else:
            print(f"Auth Failed ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def create_kimai_customer(name):
    payload = {
        "name": name, 
        "country": COUNTRY, 
        "currency": CURRENCY, 
        "timezone": TIMEZONE, 
        "visible": True
    }
    response = requests.post(f"{KIMAI_URL}/customers", headers=kimai_headers, json=payload)
    return response.json()['id'] if response.status_code in [200, 201] else None

def create_kimai_project(name, customer_id):
    payload = {
        "name": name, 
        "customer": customer_id, 
        "visible": True
    }
    response = requests.post(f"{KIMAI_URL}/projects", headers=kimai_headers, json=payload)
    return response.status_code in [200, 201]

def main():
    if not all([TOGGL_API_TOKEN, TOGGL_WORKSPACE_ID, KIMAI_URL, KIMAI_API_TOKEN]):
        print("Error: Missing environment variables. Check your .env file.")
        return

    existing_customers = get_existing_kimai_customers()
    if existing_customers is None: return

    url = f"https://api.track.toggl.com/api/v9/workspaces/{TOGGL_WORKSPACE_ID}/clients"
    toggl_res = requests.get(url, auth=(TOGGL_API_TOKEN, 'api_token'), headers=toggl_headers)
    
    if toggl_res.status_code != 200:
        print(f"Toggl Error: {toggl_res.text}")
        return

    toggl_clients = toggl_res.json()
    print(f"Found {len(toggl_clients)} clients in Toggl.")

    for t_client in toggl_clients:
        name = t_client['name']
        
        if name in existing_customers:
            print(f"[-] '{name}' already exists. Skipping customer creation.")
            customer_id = existing_customers[name]
        else:
            print(f"[+] Creating Customer: {name}...", end=" ")
            customer_id = create_kimai_customer(name)
            if not customer_id:
                print("Failed.")
                continue
            print("Done.")

        if create_kimai_project(name, customer_id):
            print(f"    [+] Project '{name}' created/verified.")
        else:
            print(f"    [!] Project '{name}' already exists.")

if __name__ == "__main__":
    main()