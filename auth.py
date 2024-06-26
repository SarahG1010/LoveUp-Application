import json
from flask import request, _request_ctx_stack,abort
from functools import wraps
from jose import jwt
print('sucess')
from urllib.request import urlopen

'''
AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'dev'
'''

AUTH0_DOMAIN = 'dev-tc7l4qq1g3f7bjju.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'loveup'


## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
#def get_token_auth_header():
   #raise Exception('Not Implemented')

def get_token_auth_header():

    auth = request.headers.get('Authorization', None)
    #print(auth)
    if not auth:
        abort(401)

    parts = auth.split(' ')
    if parts[0].lower() != 'bearer':
        abort(401)

    elif len(parts) == 1:
        abort(401)

    elif len(parts) > 2:
        abort(401)
    #print(parts[1])
    return parts[1]

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
#def check_permissions(permission, payload):
    #raise Exception('Not Implemented')

def check_permissions(permission, payload):

    if 'permissions' not in payload:
        abort(400)

    if permission not in payload['permissions']:
        abort(403)

    return True

'''
implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
#def verify_decode_jwt(token):
  #  raise Exception('Not Implemented')

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    #print('s-1')
    #print('unverified_header[kid]:{}'.format(unverified_header['kid']))
    #print(jsonurl)
    #print(jwks)
    if 'kid' not in unverified_header:
        raise AuthError({'code': 'invalid_header',
                        'description': 'Authorization malformed.'
                        }, 401)
    #print('s-1.1')
    for key in jwks['keys']:
        #print(jwks['keys'])
        #print('key:{},kid:{}'.format(key,key['kid']))
        
        if key['kid'] == unverified_header['kid']:
            rsa_key = {'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']}
    #print('s-1.2')
    #print(rsa_key)
    if rsa_key:
        try:
            payload = jwt.decode(token,
                                rsa_key,
                                algorithms=ALGORITHMS,
                                audience=API_AUDIENCE,
                                issuer='https://' + AUTH0_DOMAIN + '/')

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token Expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Invalid claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    else:
        raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to find the appropriate key.'
                }, 400)



'''
implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            #print('===token====:{}\n'.format(token))
            try:
                payload = verify_decode_jwt(token)
            except Exception as e:
                #print('s-2')
                print(e)
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator