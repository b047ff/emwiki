import os

from django.db import models
from django.conf import settings
from django.utils import timezone


class Explanation(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    explanation_dir = settings.EMWIKI_CONTENTS_EXPLANATON_DIR

    def __str__(self):
        return self.title, self.author, self.created_at, self.updated_at

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def get_explanationfile_path(self):
        return os.path.join(self.explanation_dir, f'{self.title}.txt')

    # def create_text_file(directory, file_name, text):
    #     file_path = os.path.join(directory, file_name)
    #     with open(file_path, 'w') as file:
    #         file.write(text)
   
    def commit_explanation_creates(self):
        commit_message = f'Create {self.text}\n {self.author}\n'
        settings.EMWIKI_CONTENTS_EXPLANATION_REPO.git.add(self.get_explanationfile_path())
        settings.EMWIKI_CONTENTS_EXPLANATION_REPO.index.commit(commit_message)

    def commit_explanation_changes(self):
        commit_message = f'Update {self.text}\n {self.author}\n'
        settings.EMWIKI_CONTENTS_EXPLANATION_REPO.git.add(self.get_explanationfile_path())
        settings.EMWIKI_CONTENTS_EXPLANATION_REPO.index.commit(commit_message)
