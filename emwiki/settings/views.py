from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from .models import Settings
from django.contrib.auth import get_user_model


class IndexView(TemplateView):
    template_name = 'settings/index.html'

    def get(self, request):
        user = get_user_model().objects.get(username=request.user.username)
        settings = Settings.objects.filter(user=user).first()

        if settings is not None:
            id = settings.github_id
            repository_name = settings.repository_name
            return render(request, 'settings/index.html', {'github_id': id, 'repository_name': repository_name})
        else:
            return render(request, 'settings/index.html')


class RegistrationView(TemplateView):
    template_name = 'settings/settings_registration.html'

    def post(self, request):
        if request.method == 'POST':
            user_name = get_user_model().objects.get(username=request.user.username)
            id = request.POST.get('github_id')
            repository_name = request.POST.get('repository_name')
            new_settings = Settings.objects.create(user=user_name, github_id=id, repository_name=repository_name)
            new_settings.save()

            return redirect('settings:index')


class ChangeView(TemplateView):
    template_name = 'settings/settings_change.html'

    def get(self, request):
        user = get_user_model().objects.get(username=request.user.username)
        settings = Settings.objects.filter(user=user).first()

        return render(request, 'settings/settings_change.html', {'settings': settings})

    def post(self, request):
        if request.method == 'POST':
            change_settings = Settings.objects.filter(user=get_user_model().objects.get(username=request.user.username)).first()
            change_settings.github_id = request.POST.get('github_id')
            change_settings.repository_name = request.POST.get('repository_name')
            change_settings.save()

            return redirect('settings:index')


class DevelopView(TemplateView):
    template_name = 'settings/develop.html'

    def get(self, request):
        settings = Settings.objects.filter(user=get_user_model().objects.get(username=request.user.username)).first()

        if settings is not None:
            id = settings.github_id
            repository_name = settings.repository_name

            return render(request, 'settings/develop.html', {'github_id': id, 'repository_name': repository_name})
        else:
            return render(request, 'settings/develop.html')
