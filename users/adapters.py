import shortuuid
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return super().get_login_redirect_url(request)

    def save_user(self, request, user, form, commit=True):
        uuid = shortuuid.uuid()
        user.uuid_for_google_form = uuid
        super().save_user(request, user, form, commit)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        uuid = shortuuid.uuid()
        user = sociallogin.user
        user.uuid_for_google_form = uuid
        super().save_user(request, sociallogin, form)
