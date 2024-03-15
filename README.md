# Installation Guide

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Steps

1. Clone the repository:
    ```
    git clone https://github.com/alexgoller/illumio-policy-check
    ```
2. Navigate to the project directory:
    ```
    cd illumio-policy-check
    ```
3. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```
4. Set the necessary environment variables:
    
    Variables can be set to not contaminate your shell history or have secrets floating around on the shell

    ```
    export PCE_HOST=your_pce_host
    export PCE_PORT=your_pce_port
    export PCE_ORG=1
    export PCE_API_USER=your_api_user
    export PCE_API_KEY=your_api_key
    ```
5. Run the script:
    ```
    python3 ./policy-check.py --source 10.0.1.34 --destination 10.0.0.70 --destination-port 5666  --protocol tcp
    ```
    If a Illumio rule exists for the source/destination/destination-port and protocol, the script will return 0 and output the rule(s)
    Else, the script will return 1 and you can use that in further scripts or as a status var.

6. Help:

./policy_check.py --help