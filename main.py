import http.client
import json
import base64
import datetime
import plotly.express as px
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Function to get base64-encoded credentials
def get_encoded_credentials(username, password):
    credentials = f"{username}:{password}"
    return base64.b64encode(credentials.encode()).decode()

# Function to make an API request
def make_request(conn, method, endpoint, headers):
    conn.request(method, endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

# Main step 1: function to get domains and write to a JSON file
def get_domains_and_write_to_file():
    # Get the username and password from environment variables
    username = os.getenv("COLLIBRA_USERNAME")
    password = os.getenv("COLLIBRA_PASSWORD")
    encoded_credentials = get_encoded_credentials(username, password)
    instance_name = "support-outsource-emea.collibra.com"
    conn = http.client.HTTPSConnection(instance_name)
    headers = {
        'Accept': "application/json",
        'Authorization': f"Basic {encoded_credentials}"
    }

    # Get list of domains
    logging.info(f"Collecting domains in {instance_name}")
    domains = make_request(conn, "GET", "/rest/2.0/domains", headers)

    # Filter unique domain types
    logging.info(f"Filtering unique domain types in {instance_name}")

    unique_domain_types = set()
    unique_domains = []
    for domain in domains['results']:
        domain_type = domain['type']['name']
        if domain_type not in unique_domain_types:
            unique_domain_types.add(domain_type)
            unique_domains.append(domain)

    # For each unique domain type, show asset types available in the operating model
    logging.info(f"Collecting available asset types for a domain subset in {instance_name}")
    domain_asset_types = {}
    colors=[]
    for domain in unique_domains:
        domain_id = domain['id']
        domain_type = domain['type']['name']
        # Get list of asset types
        asset_types = make_request(conn, "GET", f"/rest/2.0/assignments/domain/{domain_id}/assetTypes", headers)
        asset_type_names = []
        # if response is empty, record the empty response and continue the outer loop
        if not asset_types:
            domain_asset_types[domain_type] = asset_type_names
            continue
        # else, start inner loop: gather asset types names and colors
        else:
            for asset_type in asset_types:
                asset_type_names.append(asset_type['name'])
                colors.append(asset_type['symbolData']['color'])
            domain_asset_types[domain_type] = asset_type_names

    # Write the domain asset types data to a JSON file
    try:
        with open("domain_asset_types.json", "w") as json_file:
            json.dump(domain_asset_types, json_file, indent=4)
            logging.info("Mapping asset types to domain types complete and written to domain_asset_types.json")
    except IOError as e:
        logging.error(f"Failed to write to file: {e}")

    conn.close()

    # Main step 2: visualize the result
    logging.info("Visualizing the result")

    visualize(domain_asset_types, instance_name, colors)

# visualize the result
def visualize(domain_asset_types, instance_name, colors):

    # Prepare data for visualization
    labels = []
    sizes = []
    parents = []

    for domain, assets in domain_asset_types.items():
        for asset in assets:
            labels.append(asset)
            sizes.append(1)  # Each asset type will have the same size
            parents.append(domain)

    # Create a DataFrame for the plotly treemap
    data = {'Asset': labels, 'Size': sizes, 'Domain': parents}

    # Create a dictionary from labels and colors
    label_color_dict = dict(zip(labels, colors))
    new_pair = {'(?)':'#E8E8E8'}
    new_label_color_dict = {**new_pair, **label_color_dict}

    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a treemap
    fig = px.treemap(data, path=['Domain', 'Asset'], values='Size', color='Asset', color_discrete_map=new_label_color_dict,
                     title=f'<span style="font-size:32px; opacity:0.1">|</span><span style="opacity:0.5">    Mapping types: assets to domains</span>'
                           f'<span style="font-size:12px; opacity:0.3; float:right; margin-right:10px;">                                  '
                           f'                                                                                          '
                           f'                                                                                          '
                           f'   <b>{instance_name}</b>    {timestamp}</span>')
    fig.update_traces(hovertemplate='<b>%{label}</b><extra></extra>', marker=dict(cornerradius=10))
    fig.update_layout(margin=dict(t=78, l=25, r=25, b=25), font_family="Helvetica", title_x=0.1, paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF')
    fig.add_layout_image(
        dict(
            source="https://www.collibra.com/mfe/nav/assets/icons/logo.svg",
            xref="paper", yref="paper",
            x=0, y=1.1,
            sizex=0.07, sizey=0.07,
            xanchor="left", yanchor="top"
        )
    )
    fig.show()

if __name__ == "__main__":
    get_domains_and_write_to_file()