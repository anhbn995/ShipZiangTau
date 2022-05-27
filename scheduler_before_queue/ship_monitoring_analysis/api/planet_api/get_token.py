import requests

AUTH_URL = 'https://api.planet.com/auth/v1/experimental/public/users/authenticate'


def get_planet_auth_token(email, password):
    payload = {'email': email, 'password': password}
    r = requests.post(AUTH_URL, json=payload)
    response = r.json()
    try:
        token = response['token']
    except Exception as e:
        print(response)
        raise e
    else:
        return token
