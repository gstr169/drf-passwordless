from django.utils.module_loading import import_string
from drfpasswordless.settings import api_settings
from drfpasswordless.utils import (
    create_callback_token_for_user,
)


class TokenService(object):
    @staticmethod
    def send_token(user, alias_type, token_type, to_number=None, **message_payload):
        token = create_callback_token_for_user(user, alias_type, token_type)
        send_action = None

        if user.pk in api_settings.PASSWORDLESS_DEMO_USERS.keys():
            return True
        if alias_type == 'email':
            send_action = import_string(api_settings.PASSWORDLESS_EMAIL_CALLBACK)
        elif alias_type == 'mobile':
            send_action = import_string(api_settings.PASSWORDLESS_SMS_CALLBACK)
        # Send to alias
        if not to_number:
            to_number = getattr(user, api_settings.PASSWORDLESS_USER_MOBILE_FIELD_NAME)
        success = send_action(user, to_number, token, **message_payload)
        return success
