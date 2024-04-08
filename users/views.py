from django.http import HttpResponseRedirect
from django.views.generic import FormView
from utils.mixins import CustomLoginRequiredMixin
from .forms import UserUpdateForm

class UserChangeView(CustomLoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UserUpdateForm

    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_initial(self):
        user = self.get_object()
        return {"last_month" : user.last_month, "last_day" : user.last_day}

    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        user = self.get_object()
        user.last_month = form.cleaned_data.get('last_month')
        user.last_day = form.cleaned_data.get('last_day')
        user.save()
        return HttpResponseRedirect(self.success_url)