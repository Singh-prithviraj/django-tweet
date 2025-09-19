from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, "index.html")

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html',{'tweets':tweets})


@login_required
def tweet_create(request):
    if request.method == 'POST':
        form=TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm
    return render(request, 'tweet_form.html',{'form':form})


@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form=TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid:
            tweet=form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html',{'form':form})


@login_required
def tweet_delete(request, tweet_id):
    tweet=get_object_or_404(Tweet, id=tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_delete.html',{'tweet':tweet})


def register(request):
    if request.method == "POST" :
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect("tweet_list")
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html',{'form':form})



# search view
from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, "index.html")

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html',{'tweets':tweets})


@login_required
def tweet_create(request):
    if request.method == 'POST':
        form=TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html',{'form':form})


@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form=TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid:
            tweet=form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html',{'form':form})


@login_required
def tweet_delete(request, tweet_id):
    tweet=get_object_or_404(Tweet, id=tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_delete.html',{'tweet':tweet})


def register(request):
    if request.method == "POST" :
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect("tweet_list")
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html',{'form':form})


# enable search option

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Tweet

from django.db.models import Q

def tweet_list(request):
    query = request.GET.get("q", "").strip()  # remove whitespace
    if query:
        tweets = Tweet.objects.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        ).order_by('-created_at')
    else:
        # if query is empty, show all tweets
        tweets = Tweet.objects.all().order_by('-created_at')

    return render(request, 'tweet_list.html', {'tweets': tweets, 'query': query})


from django.http import JsonResponse
from .models import Tweet, Like, Comment
from django.contrib.auth.decorators import login_required

@login_required
def toggle_like(request, tweet_id):
    if request.method == "POST" and request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=tweet_id)
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        if not created:
            like.delete()
        return JsonResponse({'likes_count': tweet.likes.count()})
    return JsonResponse({'error': 'Unauthorized'}, status=403)
    
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tweet, Comment

@login_required
def add_comment(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(user=request.user, tweet=tweet, content=content)
        return redirect("tweet_list")  # Redirect after adding comment

    # If someone tries GET, redirect to tweet list or tweet detail
    return redirect("tweet_list")


