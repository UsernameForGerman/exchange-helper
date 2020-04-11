from django.shortcuts import render, Http404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

class ActiveStocksView(LoginRequiredMixin, View):
    template_name = ''

    def get(self, request, *args, **kwargs):
        return Http404()

    def post(self, request, *args, **kwargs):
        return Http404()