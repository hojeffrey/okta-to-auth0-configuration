import requests
import json
import yaml

def main():

    # Read the Okta API credentials and Auth0 API credentials from the YAML file
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    okta_api_token = config["okta_api_token"]
    okta_org_url = config["okta_org_url"]
    okta_app_name = config["okta_app_name"]
    auth0_domain = config["auth0_domain"]
    auth0_api_token = config["auth0_api_token"]
    auth0_connection_name = config["auth0_connection_name"]

    # Create an Okta OIDC application

    url = okta_org_url + "/api/v1/apps"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "SSWS " + okta_api_token
    }

    data = {
        "name": "oidc_client",
        "label": okta_app_name,
        "signOnMode": "OPENID_CONNECT",
        "credentials": {
        "oauthClient": {
            "token_endpoint_auth_method": "client_secret_post"
        }
        },
        "profile": {
            "appid": "auth0",
            "label": "auth0_okta"
            },
        "settings": {
        "oauthClient": {
            "client_uri": "http://" + auth0_domain,
            "logo_uri": "http://developer.okta.com/assets/images/logo-new.png",
            "redirect_uris": [
            "https://" + auth0_domain + "/oauth2/callback",
            "myapp://callback"
            ],
            "response_types": [
            "code"
            ],
            "grant_types": [
            "authorization_code"
            ],
            "application_type": "web"
        }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception("Failed to create Okta application. Response: " + response.text)

    app = response.json()
    okta_client_id = app["credentials"]["oauthClient"]["client_id"]
    okta_client_secret = app["credentials"]["oauthClient"]["client_secret"]

    # Configure Okta as an identity provider in Auth0

    url = "https://" + auth0_domain + "/api/v2/connections"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth0_api_token
    }

    data = {
    "name": auth0_connection_name,
    "strategy": "oauth2",
    "options": {
        "customHeaders": "",
        "client_id": okta_client_id,
        "client_secret": okta_client_secret,
        "authorizationURL": okta_org_url + "/oauth2/v1/authorize",
        "tokenURL": okta_org_url + "/oauth2/v1/token",
        "scope": "openid email profile",
        "scripts": {
        "fetchUserProfile": "function(accessToken, ctx, cb) {\n    const profile = {};\n    // Call OAuth2 API with the accessToken and create the profile\n    cb(null, profile);\n  }"
        }
    }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 201:
        raise Exception("Failed to configure Okta as an identity provider in Auth0. Response: " + response.text)

    print("Okta has been successfully configured as an identity provider in Auth0.")


if __name__ == "__main__":
    main()