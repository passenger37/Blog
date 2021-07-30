from django.urls import path
from . import views


app_name='topic'
urlpatterns = [
    path('index/', views.TopicIndexListView.as_view(), name='index'),
    path('topics/',views.TopicsListView.as_view(),name='topics'),
    path('topic/<int:topic_id>/',views.topic,name='topic'),
    path('newtopic/',views.new_topic,name='newtopic'),
    path('editentry/<int:entry_id>/',views.edit_entry,name='editentry'),
    path('deletetopic/<int:pk>/',views.TopicDeleteView.as_view(),name='delete_topic'),
    path('search/',views.SearchListView.as_view(),name="search"),  
    path('upvote/',views.upvote,name="upvote"),
    path('downvote/',views.downvote,name="downvote"),
    path('comment/',views.comment,name="comment"),
]
