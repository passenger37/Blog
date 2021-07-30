from accounts.models import Profile
from django.contrib import messages
from django.http.response import JsonResponse,Http404
from django.shortcuts import render,get_object_or_404
from  django.http import HttpResponseRedirect
from .models import Topic,UpVote,DownVote,Comment
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from .forms import Topicform,CommentForm
from django.urls import reverse,reverse_lazy
from django.contrib import messages




class TopicIndexListView(ListView):
	'''if all topics for all users'''
	model = Topic
	template_name = "base.html"
	paginate_by=2


class SearchListView(ListView):
	'''search bar'''
	model = Topic
	template_name = "base.html"
	context_object_name="page_obj"

	def get_queryset(self,*args, **kwargs):
		req=self.request
		query=req.GET.get('search')
		print(query)
		if query is not None:
			return Topic.objects.filter(text__icontains=query)
		return HttpResponseRedirect(reverse("topic:index"))
	

class TopicsListView(ListView):
	model = Topic
	template_name = "topic/topic.html"
	paginate_by=5

	def get_queryset(self,*args, **kwargs):
		# owner__user --> topi.owner.user
		topics=Topic.objects.filter(owner__user=self.request.user).order_by('date_added')
		return topics
	

def topic(request,topic_id):
	'''show a single topic and its entery'''
	topic=Topic.objects.get(id=topic_id)
	context={'topic':topic}
	return render(request,'topic/topics.html',context)

@login_required
def new_topic(request):
	'''adding new topic'''
	if request.method !='POST':
		form=Topicform()
	else:
		form=Topicform(request.POST)
		if form.is_valid():
			new_topic=form.save(commit=False)
			new_topic.owner_id=request.user.id
			new_topic.save()
			messages.success(request,'Successfully Added')
			return HttpResponseRedirect(reverse('topic:topics'))
	context={'form':form}
	return render(request,'topic/new_topic.html',context)

@login_required
def edit_entry(request,entry_id):
	'''To edit the entry'''
	topic=Topic.objects.get(id=entry_id)
	if topic.owner.user !=request.user:
		raise Http404
	if request.method !='POST':
		form=Topicform(instance=topic)
	else:
		form=Topicform(instance=topic,data=request.POST)
		if form.is_valid():
			print(">>>>>>>>>>>>>>>>>>>>>.. TOPIC FORM is Valid")
			form.save()
			messages.success(request,'Successfully  Submitted')
			return HttpResponseRedirect(reverse('topic:topics'))
	context={'entry':topic,'topic':topic,'form':form}
	return render(request,'topic/edit_entry.html',context)
	
class TopicDeleteView(DeleteView):
	'''Delete Topic'''
	model = Topic
	success_url=reverse_lazy('topic:topics')
	template_name='topic/confirm.html'


def upvote(request):
	'''upvote'''
	if request.method == 'POST':
		topicid=request.POST['topicid']
		topic = get_object_or_404(Topic, pk=topicid)
		try:
			user=Profile.objects.get(user=request.user)
			check=UpVote.objects.filter(user=user,topic=topic).count()
			if check >0:
				UpVote.objects.get(user=user,topic=topic).delete()
				DownVote.objects.get(user=user,topic=topic).delete()
			else:
				UpVote.objects.create(user=user,topic=topic) 
				if DownVote.objects.get(user=user,topic=topic):
					DownVote.objects.get(user=user,topic=topic).delete()
			ups=UpVote.objects.filter(topic=topic).count()
			downs=DownVote.objects.filter(topic=topic).count()
			return JsonResponse({'bool':False,'downvote':downs,'upvote':ups})
		except:
			topic.save()
	# ups=UpVote.objects.filter(topic=topic).count()
	# downs=DownVote.objects.filter(topic=topic).count()
	# return JsonResponse({'bool':True,'upvote':ups,'downvote':downs})


def downvote(request):
	'''downnvote'''
	if request.method == 'POST':
		topicid=request.POST['topicid']
		topic = get_object_or_404(Topic, pk=topicid)
		try:
			user=Profile.objects.get(user=request.user)
			check=DownVote.objects.filter(user=user,topic=topic).count()
			if check >0:
				DownVote.objects.get(user=user,topic=topic).delete()
			else:
				DownVote.objects.create(user=user,topic=topic) 
				if UpVote.objects.get(user=user,topic=topic):
					UpVote.objects.get(user=user,topic=topic).delete()
			downs=DownVote.objects.filter(topic=topic).count()
			ups=UpVote.objects.filter(topic=topic).count()
			return JsonResponse({'bool':False,'downvote':downs,'upvote':ups})
		except:
			topic.save()
	# downs=DownVote.objects.filter(topic=topic).count()
	# print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Down vote GET requested >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	# ups=UpVote.objects.filter(topic=topic).count()
	# return JsonResponse({'bool':True,'downvote':downs,'upvote':ups})

# TODO: response in comment to ajax
def comment(request):
	'''Comment'''
	if request.method=='POST':
		comment=request.POST['comment']
		topicid=request.POST['topicid']
		topic=get_object_or_404(Topic,pk=topicid)
		user=Profile.objects.get(user=request.user)
		Comment.objects.create(user=user,topic=topic,comment=comment)
		comment_data=Comment.objects.filter(topic=topic)
		print(" >>>>>>>>>>>>>>  Comment Data ",comment_data)
		return JsonResponse({'comment_data':comment_data})
	# comment_data=Comment.objects.filter(topic=topic)
	# return JsonResponse({
	# 	'comment_data':comment_data,
	# 	'bool':True		})


# Comment thread
