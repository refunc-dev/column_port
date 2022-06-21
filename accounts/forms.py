from allauth.account.forms import SignupForm
from django import forms
 
 
class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=50, label='ユーザー名')
 
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.username = request.POST.get('username')
        user.save()
        return user