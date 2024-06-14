# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`
     - can `get:drinks`
   - Manager
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

## All about Auth0
#### To get access_token for a user using auth0 API, follow the 2 steps:
1. In the application setting page: in `advanced setting--grant types`, check the `password`, and save.
2. In the  [Auth0 Dashboard > Tenant Settings](https://manage.auth0.com/dashboard/us/dev-tc7l4qq1g3f7bjju/tenant/general), set the `Default Directory` as the connections(Database) showed in your application,
   (for me is `Username-Password-Authentication`)
3. Then use the following command in terminal to get the token:
```
curl --request POST \
  --url 'https://dev-tc7l4qq1g3f7bjju.us.auth0.com/oauth/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=password \
  --data 'username={username(email)}' \
  --data 'password={password}' \
  --data 'audience={yourApiIdentifier}' \
  --data scope=read:sample \
  --data 'client_id=xNRnbFKojibgIj1NsIyWhwS7pO8uEBqb' \
  --data 'client_secret={yourClientSecret}'
```
**Reference:**
* [Authorization server not configured with default connection](https://community.auth0.com/t/authorization-server-not-configured-with-default-connection/114452)
* [Call Your API Using Resource Owner Password Flow](https://auth0.com/docs/get-started/authentication-and-authorization-flow/resource-owner-password-flow/call-your-api-using-resource-owner-password-flow?_gl=1*b8c5pe*_gcl_au*NjU2MDk5Nzc0LjE3MTgzNDU5MTU.*_ga*NzkxMzg1ODY5LjE3MTgzNDU5MTU.*_ga_QKMSDV5369*MTcxODM0NTkxNS4xLjEuMTcxODM0ODUwNi42MC4wLjA.#configure-tenant)

#### To get public access_token using auth0 API:
Just go to your API page, and find the `test` tab. Use the instuctions under this section to proceed(This is the easiest way). 
The general command is as following:
```
curl --request POST \
  --url 'https://dev-tc7l4qq1g3f7bjju.us.auth0.com/oauth/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=client_credentials \
  --data client_id=YOUR_CLIENT_ID \
  --data client_secret=YOUR_CLIENT_SECRET \
  --data audience=YOUR_API_IDENTIFIER
```
**Reference:**
* [Get Access Tokens](https://auth0.com/docs/secure/tokens/access-tokens/get-access-tokens)

#### To access my login page:
[My_login_page](https://dev-tc7l4qq1g3f7bjju.us.auth0.com/authorize?response_type=token&client_id=XPp6dF1jl8JEsaEuOnh9ZRh1fWn9xrY0&redirect_uri=http://127.0.0.1:5000)

references:
* [Introduction](https://auth0.com/docs/api/authentication?_gl=1*b8c5pe*_gcl_au*NjU2MDk5Nzc0LjE3MTgzNDU5MTU.*_ga*NzkxMzg1ODY5LjE3MTgzNDU5MTU.*_ga_QKMSDV5369*MTcxODM0NTkxNS4xLjEuMTcxODM0ODUwNi42MC4wLjA.#resource-owner-password)
* Udacity full stack web developer
  -- Identity Access Management
   -- Identity and Authentication
     --5.Implementing Auth0

#### To test the application (My API) with access_token:
1. with `curl`
```
curl --request GET \
  --url http://127.0.0.1:5000/drinks \
  --header 'authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1MdHFvUXhpeGhJZWRSM0Zob3F3ZSJ9.eyJpc3MiOiJodHRwczovL2Rldi10YzdsNHFxMWczZjdiamp1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJGakI2Nk9lazhlQ2VHQWs3R3psTzhLUklSSmNxV2VaTUBjbGllbnRzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNzE4MzQ0MTI4LCJleHAiOjE3MTg0MzA1MjgsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkZqQjY2T2VrOGVDZUdBazdHemxPOEtSSVJKY3FXZVpNIiwicGVybWlzc2lvbnMiOltdfQ.U1Y-wnaOo2TW4Noue5HsJIbGs3G0cp31P1_XHu-62OW5ALwykh5C7E0CVz9OEXosi8iBX7wUcDwBiBJ26HU34kGSsmyJCVIlvc6083ZTdwh1BBmMm1bwzXU_Lvl4jKa2raKLHjyIxSnjGNubM8GpcOC3LwssY7a1nyTmFUbJ2p3Sza42lB03M3Gl3-il9uwSJHAdW2byMicTF_Chw5PPg7hKZXp_USAZPL2Cm006btwyE3JgCu1-WPUY4ZUy6sCDC2UOnVMmw5k_uLFwlQfWO-8urNqLegYO7CS-iqS5ke-Nu0bFWembT7J6aRd2KS4klUkqRnbSK_woJ-KMNcIOSw'
```
2. with `python`
```
import http.client

conn = http.client.HTTPConnection("path_to_your_api")

headers = { 'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1MdHFvUXhpeGhJZWRSM0Zob3F3ZSJ9.eyJpc3MiOiJodHRwczovL2Rldi10YzdsNHFxMWczZjdiamp1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJGakI2Nk9lazhlQ2VHQWs3R3psTzhLUklSSmNxV2VaTUBjbGllbnRzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNzE4MzQ0MTI4LCJleHAiOjE3MTg0MzA1MjgsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkZqQjY2T2VrOGVDZUdBazdHemxPOEtSSVJKY3FXZVpNIiwicGVybWlzc2lvbnMiOltdfQ.U1Y-wnaOo2TW4Noue5HsJIbGs3G0cp31P1_XHu-62OW5ALwykh5C7E0CVz9OEXosi8iBX7wUcDwBiBJ26HU34kGSsmyJCVIlvc6083ZTdwh1BBmMm1bwzXU_Lvl4jKa2raKLHjyIxSnjGNubM8GpcOC3LwssY7a1nyTmFUbJ2p3Sza42lB03M3Gl3-il9uwSJHAdW2byMicTF_Chw5PPg7hKZXp_USAZPL2Cm006btwyE3JgCu1-WPUY4ZUy6sCDC2UOnVMmw5k_uLFwlQfWO-8urNqLegYO7CS-iqS5ke-Nu0bFWembT7J6aRd2KS4klUkqRnbSK_woJ-KMNcIOSw" }

conn.request("GET", "/", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

