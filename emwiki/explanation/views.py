import os

import json
from natsort import humansorted

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Explanation
from django.core.exceptions import ValidationError
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth import get_user_model


class IndexView(TemplateView):
    template_name = 'explanation/index.html'


class CreateView(generic.CreateView):
    model = Explanation
    fields = ['title', 'text', 'author', 'created_at', 'updated_at']


class ExplanationTitleView(View):
    def get(self, request):
        explanations = humansorted(list(Explanation.objects.all()), key=lambda a: a.title)
        return JsonResponse({'index': [
            dict(id=explanation.id, title=explanation.title) for explanation in explanations
        ]})


class ExplanationView(View):
    def get(self, request, title=None):
        if 'title' in request.GET:
            selectedExplanation = get_object_or_404(Explanation, title=request.GET.get('title'))
            selected_text = selectedExplanation.text
            return HttpResponse(selected_text)
        else:
            explanations = humansorted(list(Explanation.objects.all()), key=lambda a: a.title)
            return JsonResponse({'explanation': [
                dict(id=explanation.id, title=explanation.title, text=explanation.text) for explanation in explanations
            ]})

    def validate_explanation_title(self, blog_id, title):
        if not title:
            raise ValidationError('This field is required.')

        if len(title) > 200:
            raise ValidationError('Title must be 200 characters or less.')

        if Explanation.objects.exclude(id=blog_id).filter(title=title).exists():
            raise ValidationError('Title must be unique.')

    def post(self, request):
        post = json.loads(request.body)
        posted_id = post.get('id', None)
        posted_title = post.get('title', None)
        posted_text = post.get('text', None)
        if request.user.is_authenticated:
            username = request.user.username
            User = get_user_model()
            user = User.objects.get(username=username)

        try:
            self.validate_explanation_title(posted_id, posted_title)
        except ValidationError as e:
            errors = e.messages[0]
            return JsonResponse({'errors': errors}, status=400)

        createdExplanation = Explanation.objects.create(title=posted_title, text=posted_text, author=user)
        explanation_dir = settings.EMWIKI_CONTENTS_EXPLANATON_DIR
        file_path = os.path.join(explanation_dir, f"{posted_title}.txt")
        with open(file_path, 'w') as file:
            file.write(posted_text)
        createdExplanation.commit_explanation_creates()

        return redirect('explanation:index')


class DetailView(View):
    def get(self, request, title):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(title="temp")).replace('temp', ''),
        }
        return render(request, 'explanation/explanation_detail.html', context)


class UpdateView(View):
    def get(self, request, title):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(title="temp")).replace('temp', ''),
        }
        return render(request, 'explanation/explanation_change.html', context)

    def put(self, request, title):
        post = json.loads(request.body)
        updatedExplanation = Explanation.objects.get(title=title)
        User = get_user_model()
        username = request.user.username
        update_author = User.objects.get(username=username)
        updatedExplanation.text = post.get('text', None)
        updatedExplanation.author = update_author
        updatedExplanation.save()
        explanation_dir = settings.EMWIKI_CONTENTS_EXPLANATON_DIR
        file_path = os.path.join(explanation_dir, f"{updatedExplanation.title}.txt")
        with open(file_path, 'w') as file:
            file.write(updatedExplanation.text)
        updatedExplanation.commit_explanation_changes()
        return render(request, 'explanation/index.html')


class DeleteView(View):
    def get(self, request, title):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(title="temp")).replace('temp', ''),
        }
        return render(request, 'explanation/explanation_confirm_delete.html', context)

    def delete(self, request, title):
        deleteExplanation = Explanation.objects.get(title=title)
        deleteExplanation.delete()
        explanation_dir = settings.EMWIKI_CONTENTS_EXPLANATON_DIR
        file_path = os.path.join(explanation_dir, f"{deleteExplanation.title}.txt")
        try:
            os.remove(file_path)
            print(f"ファイル {file_path} を削除しました。")
            return render(request, 'explanation/index.html')
        except FileNotFoundError:
            print(f"ファイル {file_path} が見つかりませんでした。")
        except Exception as e:
            print(f"ファイル {file_path} の削除中にエラーが発生しました: {e}")

        # return render(request, 'explanation/index.html')
