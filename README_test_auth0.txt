# the login page
  GET https://dev-tc7l4qq1g3f7bjju.us.auth0.com/authorize?response_type=token&
client_id=XPp6dF1jl8JEsaEuOnh9ZRh1fWn9xrY0&redirect_uri=http://127.0.0.1:5000


http://127.0.0.1:5000/#access_token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9kZXYtdGM3bDRxcTFnM2Y3YmpqdS51cy5hdXRoMC5jb20vIn0..x6QqV3STb8SRYEqN.lVatoQhLF_bDBz9DBpSr_myFwP60ggjnMDQwtTM6-6zcsSiIoJIXpYN6yY8SAFcWKRJbgoW-XcWaesLBWTLdtbZ6fg216tasVNrKJyesFdI_jMfUO4YCc_IMAqr3BXzlQr9sKaDg6bDqYOQNxiTVd8LQdb7d42t7tRWXwqengvsUQHMXwTC9k4QU4XxhZEaUqZ55JCiP3heKOTPKJzlfY26h71PyUb4PxBPgm5av9tqcwPv2FMpaV7sUCizyHbLn1fB2yd6XV6Gs3PaRQxMIEHP-415URbY4BSYsRyY3eq2RjruDOEKKWk7HSZU.ckpjBjDzCTlLokeihDgOJg&expires_in=7200&token_type=Bearer

# get public access token for the accplication
##==method 1
curl --request POST \
  --url https://dev-tc7l4qq1g3f7bjju.us.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"FjB66Oek8eCeGAk7GzlO8KRIRJcqWeZM","client_secret":"Lt42jE2QhxSHyUPFj7KO_mYRTj7hIDn2KP4po2GsbgBKadU5ShbM9EkC6dWgMRSJ","audience":"http://localhost:5000","grant_type":"client_credentials"}'
##==method 2
import http.client

conn = http.client.HTTPSConnection("dev-tc7l4qq1g3f7bjju.us.auth0.com")

payload = "{\"client_id\":\"FjB66Oek8eCeGAk7GzlO8KRIRJcqWeZM\",\"client_secret\":\"Lt42jE2QhxSHyUPFj7KO_mYRTj7hIDn2KP4po2GsbgBKadU5ShbM9EkC6dWgMRSJ\",\"audience\":\"http://localhost:5000\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

## get user token
curl --request POST \
  --url 'https://dev-tc7l4qq1g3f7bjju.us.auth0.com/oauth/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=password \
  --data 'username=ziyu1211@gmail.com' \
  --data 'password=cg11Happy' \
  --data 'audience=sarahcoffee' \
  --data scope=read:sample \
  --data 'client_id=XPp6dF1jl8JEsaEuOnh9ZRh1fWn9xrY0' \
  --data 'client_secret=ZdI6ubol0XR2G-nBVwn11qKGOunP6dIADVJGWPWf-U5TLfS2z4Gi7AaCWyLkbfMd'




# test the api with token
##==method 1
curl --request GET \
  --url http://127.0.0.1:5000/drinks \
  --header 'authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1MdHFvUXhpeGhJZWRSM0Zob3F3ZSJ9.eyJpc3MiOiJodHRwczovL2Rldi10YzdsNHFxMWczZjdiamp1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJGakI2Nk9lazhlQ2VHQWs3R3psTzhLUklSSmNxV2VaTUBjbGllbnRzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNzE4MzQ0MTI4LCJleHAiOjE3MTg0MzA1MjgsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkZqQjY2T2VrOGVDZUdBazdHemxPOEtSSVJKY3FXZVpNIiwicGVybWlzc2lvbnMiOltdfQ.U1Y-wnaOo2TW4Noue5HsJIbGs3G0cp31P1_XHu-62OW5ALwykh5C7E0CVz9OEXosi8iBX7wUcDwBiBJ26HU34kGSsmyJCVIlvc6083ZTdwh1BBmMm1bwzXU_Lvl4jKa2raKLHjyIxSnjGNubM8GpcOC3LwssY7a1nyTmFUbJ2p3Sza42lB03M3Gl3-il9uwSJHAdW2byMicTF_Chw5PPg7hKZXp_USAZPL2Cm006btwyE3JgCu1-WPUY4ZUy6sCDC2UOnVMmw5k_uLFwlQfWO-8urNqLegYO7CS-iqS5ke-Nu0bFWembT7J6aRd2KS4klUkqRnbSK_woJ-KMNcIOSw'

##==method 2
python code:

import http.client

conn = http.client.HTTPConnection("path_to_your_api")

headers = { 'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1MdHFvUXhpeGhJZWRSM0Zob3F3ZSJ9.eyJpc3MiOiJodHRwczovL2Rldi10YzdsNHFxMWczZjdiamp1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJGakI2Nk9lazhlQ2VHQWs3R3psTzhLUklSSmNxV2VaTUBjbGllbnRzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNzE4MzQ0MTI4LCJleHAiOjE3MTg0MzA1MjgsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkZqQjY2T2VrOGVDZUdBazdHemxPOEtSSVJKY3FXZVpNIiwicGVybWlzc2lvbnMiOltdfQ.U1Y-wnaOo2TW4Noue5HsJIbGs3G0cp31P1_XHu-62OW5ALwykh5C7E0CVz9OEXosi8iBX7wUcDwBiBJ26HU34kGSsmyJCVIlvc6083ZTdwh1BBmMm1bwzXU_Lvl4jKa2raKLHjyIxSnjGNubM8GpcOC3LwssY7a1nyTmFUbJ2p3Sza42lB03M3Gl3-il9uwSJHAdW2byMicTF_Chw5PPg7hKZXp_USAZPL2Cm006btwyE3JgCu1-WPUY4ZUy6sCDC2UOnVMmw5k_uLFwlQfWO-8urNqLegYO7CS-iqS5ke-Nu0bFWembT7J6aRd2KS4klUkqRnbSK_woJ-KMNcIOSw" }

conn.request("GET", "/", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))