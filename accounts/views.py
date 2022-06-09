from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('top')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='accounts.backends.EmailAuthBackend')
        messages.add_message(self.request, messages.SUCCESS, '会員登録に成功しました。')
        print(user.email)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, '会員登録に失敗しました。')
        return super().form_invalid(form)