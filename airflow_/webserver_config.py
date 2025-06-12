#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Default configuration for the Airflow webserver."""

from __future__ import annotations
import os
import logging
import jwt
import requests
from base64 import b64decode
from cryptography.hazmat.primitives import serialization
from tokenize import Exponent
from airflow.www.security import AirflowSecurityManager
from flask_appbuilder import expose
from flask_appbuilder.security.views import AuthOAuthView


# from airflow.www.fab_security.manager import AUTH_LDAP
from airflow.www.fab_security.manager import AUTH_OAUTH
# from airflow.www.fab_security.manager import AUTH_OID
# from airflow.www.fab_security.manager import AUTH_REMOTE_USER

log = logging.getLogger(__name__)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None

# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
# For details on how to set up each of the following authentication, see
# http://flask-appbuilder.readthedocs.io/en/latest/security.html# authentication-methods
# for details.

# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
# AUTH_OAUTH : Is for OAuth
# AUTH_TYPE = AUTH_DB
AUTH_TYPE = AUTH_OAUTH

# Uncomment to setup Full admin role name
# AUTH_ROLE_ADMIN = 'Admin'

# Uncomment and set to desired role to enable access without authentication
# AUTH_ROLE_PUBLIC = 'Viewer'

# Will allow user self registration
AUTH_USER_REGISTRATION = True

# The recaptcha it's automatically enabled for user self registration is active and the keys are necessary
# RECAPTCHA_PRIVATE_KEY = PRIVATE_KEY
# RECAPTCHA_PUBLIC_KEY = PUBLIC_KEY

# Config for Flask-Mail necessary for user self registration
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_USE_TLS = True
# MAIL_USERNAME = 'yourappemail@gmail.com'
# MAIL_PASSWORD = 'passwordformail'
# MAIL_DEFAULT_SENDER = 'sender@gmail.com'

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Public"

# When using OAuth Auth, uncomment to setup provider(s) info
# Google OAuth example:
# OAUTH_PROVIDERS = [{
#   'name':'google',
#     'token_key':'access_token',
#     'icon':'fa-google',
#         'remote_app': {
#             'api_base_url':'https://www.googleapis.com/oauth2/v2/',
#             'client_kwargs':{
#                 'scope': 'email profile'
#             },
#             'access_token_url':'https://accounts.google.com/o/oauth2/token',
#             'authorize_url':'https://accounts.google.com/o/oauth2/auth',
#             'request_token_url': None,
#             'client_id': GOOGLE_KEY,
#             'client_secret': GOOGLE_SECRET_KEY,
#         }
# }]

CLIENT_ID='airflow'
PROVIDER_NAME = 'keycloak'
OIDC_ISSUER = 'http://localhost:8123/realms/analytics'
OIDC_ISSUER_BACKEND_URL = 'http://keycloak:8080/realms/analytics'
OIDC_BASE_URL = f"{OIDC_ISSUER}/protocol/openid-connect"
OIDC_TOKEN_URL = f"{OIDC_ISSUER_BACKEND_URL}/protocol/openid-connect/token"
JWKS_URI = f"{OIDC_ISSUER_BACKEND_URL}/protocol/openid-connect/certs"
OIDC_AUTH_URL = f"{OIDC_BASE_URL}/auth"
OAUTH_PROVIDERS = [
    {
        "name": PROVIDER_NAME,
        "icon": "fa-key",
        "token_key": "access_token",
        "remote_app": {
            "client_id": "airflow",
            "client_secret": "2rBHDPIwVby6E3vJwqPWJl4VbgtE3HR4",
            "api_base_url": OIDC_BASE_URL,
            "client_kwargs": {
                "scope": "openid email profile"
            },
            "access_token_url": OIDC_TOKEN_URL,
            "authorize_url": OIDC_AUTH_URL,
            "request_token_url": None,
            "jwks_uri":JWKS_URI
        }
    }
]
# https://flask-appbuilder.readthedocs.io/en/latest/security.html

AUTH_ROLES_SYNC_AT_LOGIN = True
AUTH_ROLES_MAPPING = {
  "airflow_admin": ["Admin"],
  "airflow_op": ["Op"],
  "airflow_user": ["User"],
  "airflow_viewer": ["Viewer"],
  "airflow_public": ["Public"],
}

req = requests.get(OIDC_ISSUER_BACKEND_URL)
key_der_base64 = req.json()["public_key"]
key_der = b64decode(key_der_base64.encode())
public_key = serialization.load_der_public_key(key_der)
class CustomAuthRemoteUserView(AuthOAuthView):
    @expose("/logout/")
    def logout(self):
        """Delete access token before logging out."""
        return super().logout()
class CustomSecurityManager(AirflowSecurityManager):
    authoauthview = CustomAuthRemoteUserView
  
    def oauth_user_info(self, provider, response):
        if provider == PROVIDER_NAME:
            token = response["access_token"]
            log.info(f"TOKEN:\n{token}")
            me = jwt.decode(token, public_key, algorithms=['HS256', 'RS256'], audience=CLIENT_ID)
            # sample of resource_access
            # {
            #   "resource_access": { "airflow": { "roles": ["airflow_admin"] }}
            # }
            groups = me["resource_access"]["airflow"]["roles"] # unsafe
            if len(groups) < 1:
                groups = ["airflow_public"]
            else:
                groups = [str for str in groups if "airflow" in str]
            userinfo = {
                "username": me.get("preferred_username"),
                "email": me.get("email"),
                "first_name": me.get("given_name"),
                "last_name": me.get("family_name"),
                "role_keys": groups,
            }
            return userinfo
        else:
            return {}
SECURITY_MANAGER_CLASS = CustomSecurityManager


# When using LDAP Auth, setup the ldap server
# AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# When using OpenID Auth, uncomment to setup OpenID providers.
# example for OpenID authentication
# OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

# ----------------------------------------------------
# Theme CONFIG
# ----------------------------------------------------
# Flask App Builder comes up with a number of predefined themes
# that you can use for Apache Airflow.
# http://flask-appbuilder.readthedocs.io/en/latest/customizing.html#changing-themes
# Please make sure to remove "navbar_color" configuration from airflow.cfg
# in order to fully utilize the theme. (or use that property in conjunction with theme)
# APP_THEME = "bootstrap-theme.css"  # default bootstrap
# APP_THEME = "amelia.css"
# APP_THEME = "cerulean.css"
# APP_THEME = "cosmo.css"
# APP_THEME = "cyborg.css"
# APP_THEME = "darkly.css"
# APP_THEME = "flatly.css"
# APP_THEME = "journal.css"
# APP_THEME = "lumen.css"
# APP_THEME = "paper.css"
# APP_THEME = "readable.css"
# APP_THEME = "sandstone.css"
# APP_THEME = "simplex.css"
# APP_THEME = "slate.css"
# APP_THEME = "solar.css"
# APP_THEME = "spacelab.css"
# APP_THEME = "superhero.css"
# APP_THEME = "united.css"
# APP_THEME = "yeti.css"