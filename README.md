# Collibra Domain and Asset Type Mapping
### What it does?
This project retrieves domain and asset type information from a Collibra instance, writes the data to a JSON file, and visualizes the result using a treemap. Example:
![Overivew](./images/overview.png)

### Why?
This project is useful for understanding the structure of your Collibra instance metamodel and the relationships between domains and asset types. It helps answering such questions as:
- What asset types do I have?
- What domain types are hosting them?
- When a new asset is created (upon ingestion from data source or when created manually) to what type of domain will it go?

The visualization helps you see the big picture and identify areas that need improvement or your special attention. Such feature is currently not available in Collibra.   

### Other features:
In the top-right corner, you can see your instance details:
![Instance details](./images/instance_details.png)

The treemap is interactive, so you can zoom in and out, and hover over the tiles to see more information:
 ![Clickable domain](./images/clickable_domain.png)

Zooming in shows the asset types within a domain:
![Enter domain](./images/enter_domain.png)

Back to the top-right corner, you can click on a photo icon and capture the whole operating model:
![Capture](./images/capture.png)

## Prerequisites

- Python 3.6+
- `pip` (Python package installer)
- `virtualenv` (optional, but recommended)

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of the project and add your Collibra credentials:
    ```env
    COLLIBRA_USERNAME=your_username
    COLLIBRA_PASSWORD=your_password
    ```

## Usage

To run the script and generate the JSON file and visualization, execute:
```sh
python main.py