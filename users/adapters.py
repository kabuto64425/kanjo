import shortuuid
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        print("login override")
        return super().get_login_redirect_url(request)

    def save_user(self, request, user, form, commit=True):
        print("save user")
        uuid = shortuuid.uuid()
        user.uuid_for_google_form = uuid
        super().save_user(request, user, form, commit)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        print("connect override")
        return super().get_login_redirect_url(request)
    
    def save_user(self, request, sociallogin, form=None):
        print("save user social")
        uuid = shortuuid.uuid()
        user = sociallogin.user
        user.uuid_for_google_form = uuid
        super().save_user(request, sociallogin, form)
