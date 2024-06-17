# Love up Application(backend version 0.0)

## Introduction
Introducing LoveUp, a revolutionary application designed to fill a crucial gap in the Chinese film industry. 
Inspired by the renowned U.S. movie rating system, LoveUp will utilize cutting-edge machine learning models(Not yet trained) 
to assess and rate Chinese children's movies. This version of the application contains necessary APIs for the backend of the APP.

## Getting Started

### Installing Dependencies

#### Python 3.11

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

Recommend working within a virtual environment whenever using Python for projects. Use following command to set up virtual environment:
```
python -m virtualenv env
source env/bin/activate
```
#### PIP Dependencies

Once virtual environment setup and running, install dependencies:

```bash
pip install -r requirements.txt
```


##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.
## Endpoints
In the API, there are 5 endpoints and 1 root route:
* **GET /:** 
>show a `Hello` message
* **GET /movies:** 
>show brief information of the movies
* **GET /movies-detail:** 
>show detailed information of the movies
* **POST /movies:** 
>add a movie to the database
* **PATCH /movies/{movie-id}:** 
>update movie(with {movie-id}) information for a specific movie
* **DELETE /movies/{movie-id}:** 
>delete a movie (with {movie-id}) from the database



## Running the server locally
#### Running in Debug mode:
In the `app.py`, found the following line and make sure `debug=True`:
```
if __name__ == '__main__':
    app.run(debug=True)
```
#### Running in regular mode(when you deploy the API):
1. In the `app.py`, found the following line:
```
if __name__ == '__main__':
    app.run(debug=True)
```
2. Change the above code to the following:
```
if __name__ == '__main__':
    app.run()
```

## Data Models
There are 2 data models in this app.
* **Movie**:

| Columns        | Description                 | Property                       |
|----------------|-----------------------------|--------------------------------|
| id             | id for movie                | integer,primary key            |
| title          | name of the movie           | string, not null               |
| year           | year of the movie           | integer, not null              |
| duration       | duration of the movie       | integer, not null              |
| pred_rating_id | pred_rating_id of the movie | integer, not null, foreign key |
| detail         | detail of the movie         | string, not null               |


* **Pred_Rating**:

| Columns        | Description                             | Property                       |
|----------------|-----------------------------------------|--------------------------------|
| id             | id for rating                           | integer,primary key            |
| type           | rating type                             | string, not null               |
| note           | note for the note                       | integer, not null              |


#### Use `psql` to check database:
The capital letter in tables will cause problems. 
If there is a capital letter in table names,use the followings cammand to select:
(Note: **Double** quote is necessary)
```
select * from "Movie"; 
```
## All about Auth0
### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain(make sure set the `Default Directory` as the `connections(Database)` showed in your application)
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:movies-detail`
   - `post:movies`
   - `patch:movies`
   - `delete:movies`
6. Create new roles for:
   - Membership
     - can `get:movies-detail`
   - Admin
     - can perform all actions
### Use Auth0 API to get access_token

#### Get public access_token:
Just go to your API page, and find the `test` tab. Use the instuctions under this section to proceed(This is the easiest way).
The general command is as following:
* With curl(All `{some word}` need to be replaced):
```
curl --request POST \
  --url 'https://{yourDomain}/oauth/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=client_credentials \
  --data client_id=YOUR_CLIENT_ID \
  --data client_secret=YOUR_CLIENT_SECRET \
  --data audience=YOUR_API_IDENTIFIER
```

* With python(All `CAPITAL word` need to be replaced):

```
def get_public_headers():
    conn = http.client.HTTPSConnection("YOUR_DOMAIN")  
    payload = "{\"client_id\":\"YOUR_CLIENT_ID\",\
                \"client_secret\":\"YOUR_CLIENT_SECRET\",\
                \"audience\":\"YOUR_API_IDENTIFIER\",\
                \"grant_type\":\"client_credentials\"}"
    
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
```
>**Important Note:** `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` can be found in your API-test section
> (This should be the `CLIENT_ID` and `CLIENT_SECRET` for the application AUTH0 
> create for test purpose, usually is a `Machine-to_Machine`application named with 
> Your API name and followed by (Test Application), i.e. for my API it is named `loveup(Test Application)`  )

Reference:
* [Get Access Tokens](https://auth0.com/docs/secure/tokens/access-tokens/get-access-tokens)


#### Get access_token for different users:
1. In the application setting page: in `advanced setting--grant types`, check the `password`, and save.
2. In the  [Auth0 Dashboard > Tenant Settings](https://manage.auth0.com/dashboard/us/dev-tc7l4qq1g3f7bjju/tenant/general), set the `Default Directory` as the connections(Database) showed in your application,
   (for me is `Username-Password-Authentication`)
3. Then use the following command in terminal to get the token:

* with curl (All `{some word}` need to be replaced):

```
curl --request POST \
  --url 'https://{yourDomain}/oauth/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=password \
  --data 'username={username(email)}' \
  --data 'password={password}' \
  --data 'audience={yourApiIdentifier}' \
  --data scope=read:sample \
  --data 'client_id={yourClientId}' \
  --data 'client_secret={yourClientSecret}'
```
* with python (All `CAPITAL word` need to be replaced):
```
def get_member_headers():
    conn = http.client.HTTPSConnection("YOUR_DOMAIN")

    payload = "{\"client_id\":\"YOUR_CLIENT_ID\",\
    \"client_secret\":\"YOUR_CLIENT_SECRET\",\
    \"audience\":\"YOUR_API_IDENTIFIER\",\
    \"grant_type\":\"password\",\
    \"username\":\"USER_NAME(OR EMAIL)\",\
    \"password\":\"PASSWORD\",\
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
```
Reference:
* [Authorization server not configured with default connection](https://community.auth0.com/t/authorization-server-not-configured-with-default-connection/114452)
* [Call Your API Using Resource Owner Password Flow](https://auth0.com/docs/get-started/authentication-and-authorization-flow/resource-owner-password-flow/call-your-api-using-resource-owner-password-flow?_gl=1*b8c5pe*_gcl_au*NjU2MDk5Nzc0LjE3MTgzNDU5MTU.*_ga*NzkxMzg1ODY5LjE3MTgzNDU5MTU.*_ga_QKMSDV5369*MTcxODM0NTkxNS4xLjEuMTcxODM0ODUwNi42MC4wLjA.#configure-tenant)



#### To access my login page*:
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
## Deploy API on Render
#### Step 1: Create a database 
#### Step 2: Create a webservice
Add a environment viriable `DATABASE_URL` (get from the create databse)
#### Step 3: waiting for built and deploy

#### Trouble shooting:
1. Add `gunicorn` to requiement.txt
2. Add the following command to the `Start Command` section when deploy from github repo:
```
gunicorn app:app
```
The command `gunicorn app:app` is used to start a Gunicorn server for a Python web application named app.
>* The first app refers to the Python module (file) containing your Flask or Django application.
> 
>* The second app refers to the variable within that module that represents your application instance.
> 
This command tells Gunicorn to start a server using the WSGI application object named app found in the module app. Gunicorn is a popular WSGI HTTP server for Python web applications. It's often used in production environments to serve web applications built with Flask, Django, and other frameworks.

## Runing Unit test
In the main directory, you can run unit test (without actually run the API in the server). Follow this steps:
1. Set up the virtual environment
2. Run the following command in the terminal:
```
python test_app.py
```
* About test_app.py:
The test_app.py will run in the following flow:
1. Get three different hearders for different roles: 
> -- **public role**: can get movies, but not allowed to access movie details and do all other operations 
> 
>-- **membership role**: can get movies and movie details, but not allowed to do all other operations
> 
> -- **admin role**: allowed to get movies, get movie details, add movies, update movies and delete movies

2. Set up test database (in class level): `movie_child_test`
3. Run the test with test_client, and after each test, run the `tear_down` function to rollback the database.
>**Important Note:** The test will run in parallel, so if the database is drop and create in each test(i.e. NOT set up in `class` level), it may 
> create conflicts and result in a error. The database **MUST BE** set up in **CLASS** level!!

