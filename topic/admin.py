from django.contrib import admin
from .models import Topic,UpVote,DownVote,Comment

admin.site.register(Topic)

class UpVoteAdmin(admin.ModelAdmin):
    list_display=['user','topic']
admin.site.register(UpVote,UpVoteAdmin)
    

class DownVoteAdmin(admin.ModelAdmin):
    list_display=['user','topic']
admin.site.register(DownVote,DownVoteAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_display=['user','comment']
admin.site.register(Comment,CommentsAdmin)
