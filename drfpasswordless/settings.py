from django.conf import settings
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'PASSWORDLESS_AUTH', None)

DEFAULTS = {
    # --- MANDATORY SETTINGS --- #
    # The email the callback token is sent from
    'PASSWORDLESS_EMAIL_NOREPLY_ADDRESS': None,

    # Your twilio number that sends the callback tokens.
    'PASSWORDLESS_MOBILE_NOREPLY_NUMBER': None,

    # --- GENERAL SETTINGS --- #

    # Allowed auth types, can be EMAIL, MOBILE, or both.
    'PASSWORDLESS_AUTH_TYPES': ['EMAIL', 'MOBILE'],

    # URL Prefix for Authentication Endpoints
    'PASSWORDLESS_AUTH_PREFIX': 'auth/',

    #  URL Prefix for Verification Endpoints
    'PASSWORDLESS_VERIFY_PREFIX': 'auth/verify/',

    #  URL Prefix for Change Endpoints
    'PASSWORDLESS_CHANGE_PREFIX': 'auth/change/',

    # Amount of time that tokens last, in seconds
    'PASSWORDLESS_TOKEN_EXPIRE_TIME': 15 * 60,

    # The user's email field name
    'PASSWORDLESS_USER_EMAIL_FIELD_NAME': 'email',

    # The user's mobile field name
    'PASSWORDLESS_USER_MOBILE_FIELD_NAME': 'mobile',

    # Marks itself as verified the first time a user completes auth via token.
    # Automatically unmarks itself if email is changed.
    'PASSWORDLESS_USER_MARK_EMAIL_VERIFIED': False,
    'PASSWORDLESS_USER_EMAIL_VERIFIED_FIELD_NAME': 'email_verified',

    # Marks itself as verified the first time a user completes auth via token.
    # Automatically unmarks itself if mobile number is changed.
    'PASSWORDLESS_USER_MARK_MOBILE_VERIFIED': False,
    'PASSWORDLESS_USER_MOBILE_VERIFIED_FIELD_NAME': 'mobile_verified',

    # Configurable token length.
    'PASSWORDLESS_CALLBACK_TOKEN_LENGTH': 6,

    # Token Generation Retry Count
    'PASSWORDLESS_TOKEN_GENERATION_ATTEMPTS': 3,

    # Automatically send verification email or sms when a user changes their alias.
    'PASSWORDLESS_AUTO_SEND_VERIFICATION_TOKEN': False,

    # Registers previously unseen aliases as new users.
    'PASSWORDLESS_REGISTER_NEW_USERS': True,

    # Context Processors for Email Template
    'PASSWORDLESS_CONTEXT_PROCESSORS': [],

    # --- MESSAGES SECTION --- #

    # LOGIN MESSAGES
    # The email subject
    'PASSWORDLESS_EMAIL_SUBJECT': "Your Login Token",
    # A plaintext email message overridden by the html message. Takes one string.
    'PASSWORDLESS_EMAIL_PLAINTEXT_MESSAGE': "Enter this token to sign in: %s",
    # The email template name.
    'PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE_NAME': "passwordless_default_token_email.html",

    # The message sent to mobile users logging in. Takes one string.
    'PASSWORDLESS_MOBILE_MESSAGE': "Use this code to log in: %s",

    # VERIFICATION MESSAGES
    # The verification email subject
    'PASSWORDLESS_EMAIL_VERIFICATION_SUBJECT': "Your Verification Token",
    # A plaintext verification email message overridden by the html message. Takes one string.
    'PASSWORDLESS_EMAIL_VERIFICATION_PLAINTEXT_MESSAGE': "Enter this verification code: %s",
    # The verification email template name.
    'PASSWORDLESS_EMAIL_VERIFICATION_TOKEN_HTML_TEMPLATE_NAME': "passwordless_default_verification_token_email.html",

    # The message sent to mobile users verification. Takes one string.
    'PASSWORDLESS_MOBILE_VERIFICATION_MESSAGE': "Enter this verification code: %s",

    # CHANGE MESSAGES
    # The change email subject
    'PASSWORDLESS_EMAIL_CHANGE_SUBJECT': "Your Verification Token",
    # A plaintext change email message overridden by the html message. Takes one string.
    'PASSWORDLESS_EMAIL_CHANGE_PLAINTEXT_MESSAGE': "Enter this verification code: %s",
    # The change email template name.
    'PASSWORDLESS_EMAIL_CHANGE_TOKEN_HTML_TEMPLATE_NAME': "passwordless_default_change_token_email.html",

    # The message sent to mobile users verification. Takes one string.
    'PASSWORDLESS_MOBILE_CHANGE_MESSAGE': "Enter this verification code: %s",

    # --- TESTING SETTINGS --- #

    # Suppresses actual SMS for testing
    'PASSWORDLESS_TEST_SUPPRESSION': False,

    # Testing mode (every token applicable)
    'PASSWORDLESS_TEST_MODE': False,

    # List with incorrect codes (integer, please) for the test mode.
    'PASSWORDLESS_TEST_CODE_INCORRECT': [],

    # A dictionary of demo user's primary key mapped to their static pin
    'PASSWORDLESS_DEMO_USERS': {},

    # --- ADVANCED SETTINGS --- #

    # What function is called to construct an authentication tokens when
    # exchanging a passwordless token for a real user auth token.
    'PASSWORDLESS_AUTH_TOKEN_CREATOR': 'drfpasswordless.utils.create_authentication_token',

    # What function is called to construct a serializer for drf tokens when
    # exchanging a passwordless token for a real user auth token.
    'PASSWORDLESS_AUTH_TOKEN_SERIALIZER': 'drfpasswordless.serializers.TokenResponseSerializer',

    'PASSWORDLESS_EMAIL_CALLBACK': 'drfpasswordless.utils.send_email_with_callback_token',
    'PASSWORDLESS_SMS_CALLBACK': 'drfpasswordless.utils.send_sms_with_callback_token',
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE',
    'PASSWORDLESS_CONTEXT_PROCESSORS',
)

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
