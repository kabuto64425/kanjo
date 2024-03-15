from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserUpdateForm

class UserChangeView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UserUpdateForm

    success_url = '/'

    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'nick_name' : self.request.user.nick_name,
        })
        print(kwargs)
        return kwargs