import logging
from django.utils.module_loading import import_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from drfpasswordless.models import CallbackToken
from drfpasswordless.settings import api_settings
from drfpasswordless.serializers import (
    EmailAuthSerializer,
    MobileAuthSerializer,
    EmailVerificationSerializer,
    MobileVerificationSerializer,
    EmailChangeSerializer,
    MobileChangeSerializer,
    CallbackTokenAuthSerializer,
    CallbackTokenVerificationSerializer,
    CallbackTokenChangeSerializer,
)
from drfpasswordless.services import TokenService

logger = logging.getLogger(__name__)

# TODO: separate views to different files.

"""
Abstract Obtain Callback tokens
"""


class AbstractBaseObtainCallbackToken(APIView):
    """
    This returns a 6-digit callback token we can trade for a user's Auth Token.
    """
    success_response = "A login token has been sent to you."
    failure_response = "Unable to send you a login code. Try again later."

    message_payload = {}

    @property
    def serializer_class(self):
        # Our serializer depending on type
        raise NotImplementedError

    @property
    def alias_type(self):
        # Alias Type
        raise NotImplementedError

    @property
    def token_type(self):
        # Token Type
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        if self.alias_type.upper() not in api_settings.PASSWORDLESS_AUTH_TYPES:
            # Only allow auth types allowed in settings.
            logger.debug('Not allowed auth type in settings.')
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            # Validate -
            user = serializer.validated_data['user']
            # Create and send callback token
            success = TokenService.send_token(user, self.alias_type, self.token_type,
                                              **self.message_payload)

            # Respond With Success Or Failure of Sent
            if success:
                status_code = status.HTTP_200_OK
                response_detail = self.success_response
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response_detail = self.failure_response
            return Response({'detail': response_detail}, status=status_code)
        else:
            return Response(serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST)


class AbstractChangeCallbackToken(AbstractBaseObtainCallbackToken):
    def post(self, request, *args, **kwargs):
        if self.alias_type.upper() not in api_settings.PASSWORDLESS_AUTH_TYPES:
            # Only allow auth types allowed in settings.
            logger.debug('Not allowed auth type in settings.')
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            # Validate -
            user = serializer.validated_data['user']
            # Create and send callback token
            success = TokenService.send_token(
                user,
                self.alias_type,
                self.token_type,
                serializer.validated_data['mobile'],
                **self.message_payload,
            )

            # Respond With Success Or Failure of Sent
            if success:
                status_code = status.HTTP_200_OK
                response_detail = self.success_response
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response_detail = self.failure_response
            return Response({'detail': response_detail}, status=status_code)
        else:
            return Response(serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST)


"""
Login Obtain Callback tokens
"""


class ObtainEmailCallbackToken(AbstractBaseObtainCallbackToken):
    """
    Send token to user by e-mail.

    Receive: email
    Response: message or detail
    This returns a 6-digit callback token we can trade for a user's Auth Token.
    """
    permission_classes = (AllowAny,)
    serializer_class = EmailAuthSerializer
    success_response = "A login token has been sent to your email."
    failure_response = "Unable to email you a login code. Try again later."

    alias_type = 'email'
    token_type = CallbackToken.TOKEN_TYPE_AUTH

    email_subject = api_settings.PASSWORDLESS_EMAIL_SUBJECT
    email_plaintext = api_settings.PASSWORDLESS_EMAIL_PLAINTEXT_MESSAGE
    email_html = api_settings.PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE_NAME
    message_payload = {'email_subject': email_subject,
                       'email_plaintext': email_plaintext,
                       'email_html': email_html}


class ObtainMobileCallbackToken(AbstractBaseObtainCallbackToken):
    """
    Send token to user by SMS.

    Receive: mobile
    Response: message or detail
    This returns a 6-digit callback token we can trade for a user's Auth Token.
    """
    permission_classes = (AllowAny,)
    serializer_class = MobileAuthSerializer
    success_response = "We texted you a login code."
    failure_response = "Unable to send you a login code. Try again later."

    alias_type = 'mobile'
    token_type = CallbackToken.TOKEN_TYPE_AUTH

    mobile_message = api_settings.PASSWORDLESS_MOBILE_MESSAGE
    message_payload = {'mobile_message': mobile_message}


"""
Verification Obtain Callback tokens
"""


class ObtainEmailVerificationCallbackToken(AbstractBaseObtainCallbackToken):
    """
    Send token to user by e-mail for verification.

    Receive: Nothing
    Response: message or detail
    This returns a 6-digit callback token we can trade for a user's Auth Token.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailVerificationSerializer
    success_response = "A verification token has been sent to your email."
    failure_response = "Unable to email you a verification code. Try again later."

    alias_type = 'email'
    token_type = CallbackToken.TOKEN_TYPE_VERIFY

    email_subject = api_settings.PASSWORDLESS_EMAIL_VERIFICATION_SUBJECT
    email_plaintext = api_settings.PASSWORDLESS_EMAIL_VERIFICATION_PLAINTEXT_MESSAGE
    email_html = api_settings.PASSWORDLESS_EMAIL_VERIFICATION_TOKEN_HTML_TEMPLATE_NAME
    message_payload = {
        'email_subject': email_subject,
        'email_plaintext': email_plaintext,
        'email_html': email_html
    }


class ObtainMobileVerificationCallbackToken(AbstractBaseObtainCallbackToken):
    """
    Send token to user by SMS for verification.

    Receive: Nothing
    Response: message or detail
    This returns a 6-digit callback token we can trade for a user's Auth Token.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MobileVerificationSerializer
    success_response = "We texted you a verification code."
    failure_response = "Unable to send you a verification code. Try again later."

    alias_type = 'mobile'
    token_type = CallbackToken.TOKEN_TYPE_VERIFY

    mobile_message = api_settings.PASSWORDLESS_MOBILE_VERIFICATION_MESSAGE
    message_payload = {'mobile_message': mobile_message}


"""
Change Obtain Callback tokens
"""


class ObtainEmailChangeCallbackToken(AbstractChangeCallbackToken):
    """
    Send token to user by e-mail for changing.

    Receive: email
    Response: message or detail
    This returns a 6-digit callback token we can trade for a user's Auth Token.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailChangeSerializer
    success_response = "A verification token has been sent to your email."
    failure_response = "Unable to email you a verification code. Try again later."

    alias_type = 'email'
    token_type = CallbackToken.TOKEN_TYPE_CHANGE

    email_subject = api_settings.PASSWORDLESS_EMAIL_VERIFICATION_SUBJECT
    email_plaintext = api_settings.PASSWORDLESS_EMAIL_VERIFICATION_PLAINTEXT_MESSAGE
    email_html = api_settings.PASSWORDLESS_EMAIL_VERIFICATION_TOKEN_HTML_TEMPLATE_NAME
    message_payload = {
        'email_subject': email_subject,
        'email_plaintext': email_plaintext,
        'email_html': email_html
    }


class ObtainMobileChangeCallbackToken(AbstractChangeCallbackToken):
    """
    Send token to user by SMS for changing.

    Receive: mobile
    Response: message or detail
    This returns a 6-digit callback token we can trade for a user's Auth Token.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MobileChangeSerializer
    success_response = "We texted you a verification code."
    failure_response = "Unable to send you a verification code. Try again later."

    alias_type = 'mobile'
    token_type = CallbackToken.TOKEN_TYPE_CHANGE

    mobile_message = api_settings.PASSWORDLESS_MOBILE_CHANGE_MESSAGE
    message_payload = {'mobile_message': mobile_message}


"""
Obtain Auth tokens
"""


class AbstractBaseObtainAuthToken(APIView):
    """
    This is a duplicate of rest_framework's own ObtainAuthToken method.
    Instead, this returns an Auth Token based on our 6 digit callback token and source.
    """
    serializer_class = None

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token_creator = import_string(api_settings.PASSWORDLESS_AUTH_TOKEN_CREATOR)
            (token, _) = token_creator(user)

            if token:
                TokenSerializer = import_string(
                    api_settings.PASSWORDLESS_AUTH_TOKEN_SERIALIZER)
                token_serializer = TokenSerializer(data=token.__dict__, partial=True)
                if token_serializer.is_valid():
                    # Return our key for consumption.
                    return Response(token_serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error(
                "Couldn't log in unknown user. Errors on serializer: {}".format(
                    serializer.error_messages))
        return Response({'detail': 'Couldn\'t log you in. Try again later.'},
                        status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthTokenFromCallbackToken(AbstractBaseObtainAuthToken):
    """
    Verify token received from user for login/registration purpose.

    Receive: email or mobile, token
    Response: token
    This is a duplicate of rest_framework's own ObtainAuthToken method.
    Instead, this returns an Auth Token based on our callback token and source.
    """
    permission_classes = (AllowAny,)
    serializer_class = CallbackTokenAuthSerializer


class VerifyAliasFromCallbackToken(APIView):
    """
    Verify token received from user and verify alias.

    Receive: email or mobile, token
    Response: message
    This verifies an alias on correct callback token entry using the same logic as auth.
    Should be refactored at some point.
    """
    serializer_class = CallbackTokenVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'user_id': self.request.user.id})
        if serializer.is_valid(raise_exception=True):
            return Response({'detail': 'Alias verified.'}, status=status.HTTP_200_OK)
        else:
            logger.error(
                "Couldn't verify unknown user. Errors on serializer: {}".format(
                    serializer.error_messages))

        return Response({'detail': 'We couldn\'t verify this alias. Try again later.'},
                        status.HTTP_400_BAD_REQUEST)


class ChangeAliasFromCallbackToken(APIView):
    """
    Verify token received from user and change alias.

    Receive: email or mobile, token
    Response: message
    This verifies an alias on correct callback token entry using the same logic as auth.
    Should be refactored at some point.
    """
    serializer_class = CallbackTokenChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'user_id': self.request.user.id}
        )
        if serializer.is_valid(raise_exception=True):
            return Response({'detail': 'Alias changed.'}, status=status.HTTP_200_OK)
        else:
            logger.error(
                "Couldn't change unknown user. Errors on serializer: {}".format(
                    serializer.error_messages))

        return Response({'detail': 'We couldn\'t change this alias. Try again later.'},
                        status.HTTP_400_BAD_REQUEST)
