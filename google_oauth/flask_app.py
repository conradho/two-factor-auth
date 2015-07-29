"""
references:
    to understand api calls https://developers.google.com/oauthplayground/
    setup project > api & auth > oauth credentials at https://console.developers.google.com
"""
from flask import Flask, Response, redirect, request
import requests
import os


app = Flask(__name__)

# this is the initial page for the enduser to navigate to
@app.route('/')
def redirect_to_google_oauth_login():
    # download json file from google console oauth credentials page to see what the auth_uri is
    redirect_url = 'https://accounts.google.com/o/oauth2/auth'
    query_params = {
        'response_type': 'code',
        'client_id': os.environ['GOOGLE_OAUTH_CLIENT_ID'],
        'redirect_uri': 'https://conrad.pythonanywhere.com/oauth2callback',
        # for the scopes, check it out at https://developers.google.com/oauthplayground/
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        ## 'access_type': 'offline',
        'state': 'lalalalal1',
    }
    final_url = requests.Request(url=redirect_url, params=query_params).prepare().url
    return redirect(final_url)

@app.route('/oauth2callback')
def google_oauth2_authcode_callback():
    """
    this url is the redirect URI that you setup on google developers console
    google hits this after enduser has given permission, and first gives you an auth code
    you take this auth code and swap it for an access token (and also maybe a refresh token)
    """
    if 'error' in request.args:
        return Response('oh so sad')

    auth_code = request.args['code']

    # download json file from google console oauth credentials page to see what the token_uri is
    oauth_link = 'https://accounts.google.com/o/oauth2/token'
    post_params = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': os.environ['GOOGLE_OAUTH_CLIENT_ID'],
        'client_secret': os.environ['GOOGLE_OAUTH_CLIENT_SECRET'],
        'redirect_uri': 'https://conrad.pythonanywhere.com/oauth2callback',
        # the same redirect_uri that google just hit
    }

    result = requests.post(oauth_link, data=post_params).json()
    access_token = result['access_token']  # also has other stuff like token_id

    # now you can hit various google api's that you have permission for to get info
    google_plus_user_info_api = 'https://www.googleapis.com/userinfo/v2/me'
    hidden_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    user_info = requests.get(google_plus_user_info_api, headers=hidden_headers).json()
    return Response('cool- your email is {}'.format(user_info['email']))


