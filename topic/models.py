from django.db import models
# from django.contrib.auth.models import User
from accounts.models import Profile
# from mptt.models import MPTTModel, TreeForeignKey


class Topic(models.Model):
    text=models.CharField( max_length=200)
    date_added=models.DateTimeField(auto_now=True)
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='topic_user')
    entry=models.TextField(default="")

    def __str__(self):
        return self.text

class UpVote(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="upvote_user")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class DownVote(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="downvote_user")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="comment_user")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    comment=models.TextField(default='')
    date_added=models.DateTimeField(auto_now=True)


# class CommentThread(MPTTModel):
#     parent_comment=TreeForeignKey(Comment,null=True, blank=True, related_name='children')
#     class MPTTMeta:
#         order_insertion_by=['date_added']