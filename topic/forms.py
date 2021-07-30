from django import forms
from django.db import models
from django.forms import fields
from .models import Topic,Comment
# from models import CommentThread


class Topicform(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['text','entry']
        labels={"text":"",'entry':""}


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['user','comment']



# class MPTTCommentForm(CommentForm):
#     parent = forms.ModelChoiceField(queryset=CommentThread.objects.all(), required=False, widget=forms.HiddenInput)

#     def get_comment_model(self):
#         # Use our custom comment model instead of the built-in one.
#         return CommentThread

#     def get_comment_create_data(self):
#         # Use the data of the superclass, and add in the parent field field
#         data = super(MPTTCommentForm, self).get_comment_create_data()
#         data['parent_comment'] = self.cleaned_data['parent_comment']
#         return data
