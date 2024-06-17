import http.client
import json
from flask import jsonify

def get_public_headers():
    conn = http.client.HTTPSConnection("dev-tc7l4qq1g3f7bjju.us.auth0.com")

    #payload = "{\"client_id\":\"FjB66Oek8eCeGAk7GzlO8KRIRJcqWeZM\",\"client_secret\":\"Lt42jE2QhxSHyUPFj7KO_mYRTj7hIDn2KP4po2GsbgBKadU5ShbM9EkC6dWgMRSJ\",\"audience\":\"http://localhost:5000\",\"grant_type\":\"client_credentials\"}"
    payload = "{\"client_id\":\"jhkv1ygYAfmMYHkrKD9RbONqf54BLsW2\",\"client_secret\":\"5svEOdXkXlDzQBaE-ftky3-ZtH3pG4qm19eMyUnluJlaynmRMjG0Bl6z0kHMF3l3\",\"audience\":\"loveup\",\"grant_type\":\"client_credentials\"}"
    #payload = "{\"client_id\":\"XPp6dF1jl8JEsaEuOnh9ZRh1fWn9xrY0\",\"client_secret\":\"ZdI6ubol0XR2G-nBVwn11qKGOunP6dIADVJGWPWf-U5TLfS2z4Gi7AaCWyLkbfMd\",\"audience\":\"loveup\",\"grant_type\":\"client_credentials\"}"

    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    response_str = res.read().decode("utf-8")
    # Parse the JSON string into a Python dictionary
    response_dict = json.loads(response_str)
    # Extract the access_token
    access_token = response_dict['access_token']
    token_type = response_dict['token_type']
    #print(token_type)
    header_str = '{} {}'.format(token_type,access_token)
    #print(header_str)
    
    public_headers = {'authorization': header_str}
    return public_headers


def get_member_headers():
    conn = http.client.HTTPSConnection("dev-tc7l4qq1g3f7bjju.us.auth0.com")

    payload = "{\"client_id\":\"XPp6dF1jl8JEsaEuOnh9ZRh1fWn9xrY0\",\
    \"client_secret\":\"ZdI6ubol0XR2G-nBVwn11qKGOunP6dIADVJGWPWf-U5TLfS2z4Gi7AaCWyLkbfMd\",\
    \"audience\":\"loveup\",\
    \"grant_type\":\"password\",\
    \"username\":\"cghappy1211@gmail.com\",\
    \"password\":\"cg22Happy\",\
    \"scope\":\"read:sample\"}"

    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    response_str = res.read().decode("utf-8")
    # Parse the JSON string into a Python dictionary
    response_dict = json.loads(response_str)
    #print(response_dict)
    # Extract the access_token
    access_token = response_dict['access_token']
    token_type = response_dict['token_type']

    header_str = '{} {}'.format(token_type,access_token)
    #print(header_str)
    
    member_headers = {'authorization': header_str}
    return member_headers


def get_admin_headers():
    conn = http.client.HTTPSConnection("dev-tc7l4qq1g3f7bjju.us.auth0.com")

    payload = "{\"client_id\":\"XPp6dF1jl8JEsaEuOnh9ZRh1fWn9xrY0\",\
    \"client_secret\":\"ZdI6ubol0XR2G-nBVwn11qKGOunP6dIADVJGWPWf-U5TLfS2z4Gi7AaCWyLkbfMd\",\
    \"audience\":\"loveup\",\
    \"grant_type\":\"password\",\
    \"username\":\"ziyu1211@gmail.com\",\
    \"password\":\"cg11Happy\",\
    \"scope\":\"read:sample\"}"

    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    response_str = res.read().decode("utf-8")
    # Parse the JSON string into a Python dictionary
    response_dict = json.loads(response_str)
    #print(response_dict)
    # Extract the access_token
    access_token = response_dict['access_token']
    token_type = response_dict['token_type']

    header_str = '{} {}'.format(token_type,access_token)
    print(header_str)
    
    admin_headers = {'authorization': header_str}
    return admin_headers

#get_admin_headers()

