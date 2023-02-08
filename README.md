# Okta OIDC Application and Auth0 Social Connection Configuration
This repository contains a Python script that creates an OIDC application in Okta and configures it as a social connection in Auth0.

## Requirements

- Python 3.x
- Requests library
- PyYAML library (optional, if you want to store the credentials in a YAML file)

## Usage

1. Clone the repository: `git clone https://github.com/<username>/okta-auth0-configuration.git`
2. Install the required libraries: `pip install requests` and `pip install pyyaml` (if you want to use the YAML file)
3. Store your Okta API credentials, Auth0 API credentials, Okta Url, Auth0 URL, Okta Applciation Name, and Auth0 Connection name in a file named `config.yaml` in the following format:
```
okta_api_token: "Insert Okta API Token"
okta_org_url: "https://YourComapnyURL.okta.com"
okta_app_name: "The app name that you want in Okta"
auth0_domain: "YourComapnyURL.us.auth0.com"
auth0_api_token: "Insert Auth0 API Token"
auth0_connection_name: "The connection name that you want in auth0"
```
4. Run the script: `python okta-auth0-configuration.py`
