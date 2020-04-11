from django.shortcuts import render, Http404, HttpResponse
from django.views import View
from .forms import UserAuthenticationForm
from django.contrib.auth import authenticate, login


class UserLoginView(View):
    template_name = 'auth/login.html'
    authentication_form = UserAuthenticationForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        return Http404()


    def post(self, request, *args, **kwargs):
        authentication_form = self.authentication_form(request.POST)
        if authentication_form.is_valid():
            data = authentication_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('sign in successfully')

        return HttpResponse('Invalid sign in')

class UserRegisterView(View):
    template_name = ''
    register_form = None

    def get(self, request, *args, **kwargs):
        return Http404()

    def post(self, request, *args, **kwargs):
        return Http404()
