# Collibra Domain and Asset Type Mapping

This project retrieves domain and asset type information from a Collibra instance, writes the data to a JSON file, and visualizes the result using a treemap.

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