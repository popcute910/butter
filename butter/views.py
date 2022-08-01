from audioop import reverse
from datetime import datetime
import genericpath
from pyexpat import model
from turtle import end_fill, mode
from django.forms import models
from django.http import HttpResponseRedirect, request
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth import get_user_model
# Model
from .models import MyUser, Connection, Post

# View
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import DetailView, UpdateView, ListView

# Form
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import login, authenticate
from .forms import LoginForm, MyPasswordChangeForm, PostForm, SignUpForm, UserUpdateForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import BaseUpdateView

from django.contrib import messages

from .helpers import get_current_user

@login_required
def home(request):
    following_user_list = Connection.objects.filter(follower__username=request.user.username)
    following_user = [user.following for user in following_user_list]

    posts = []
    for user in following_user:
        following_posts = Post.objects.filter(post_user=user)
        posts.extend(following_posts)

    my_posts = Post.objects.filter(post_user__username=request.user.username)
    posts.extend(my_posts)

    # 降順並び替え
    sorted_posts = sorted(posts, key=lambda x: x.created_date, reverse=True)

    # 何分前？
    # today = datetime.datetime.now(datetime.timezone.utc)
    # gap = []
    # gap_day = []
    # for post in sorted_posts:
    #     gap_from_today = today - post.created_date
    #     gap.extend(gap_from_today)
    #     gap_day.extend(gap.seconds)
    
    post_myusers = [user.post_user for user in sorted_posts]
    post_info =zip(sorted_posts, post_myusers)
    context = {'post_info': post_info,}

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_user = request.user
            post.created_date = datetime.now()
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    context['form'] = form
        
    # return render(request, 'butter/post_new.html', {'form': form})


    return render(request, 'butter/home.html', context)


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = MyUser
    template_name = 'butter/profile_posts.html'
    context_object_name = 'user_detail'

    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'username'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs): # ※(1)
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        # プロフィールのユーザー名
        username = self.kwargs['username']
        context['username'] = username
        # ログインユーザー名
        context['user'] = get_current_user(self.request) # ※(2)
        context['following'] = Connection.objects.filter(follower__username=username).count()
        context['follower'] = Connection.objects.filter(following__username=username).count()

        following_user_list = Connection.objects.filter(follower__username=username)
        # Conectionモデルのfollowingのusernameを取得
        following_username = [f'{user.following}' for user in following_user_list]
        # 上記usernameをMyUserモデルを参照してユーザーを取得
        myuser_following_username = [MyUser.objects.get(username=user) for user in following_username]
        context['following_username'] = myuser_following_username

        follower_user_list = Connection.objects.filter(following__username=username)
        # Conectionモデルのfollowerのusernameを取得
        follower_username = [f'{user.follower}' for user in follower_user_list]
        # 上記usernameをMyUserモデルを参照してユーザーを取得
        myuser_follower_username = [MyUser.objects.get(username=user) for user in follower_username]
        context['follower_username'] = myuser_follower_username

        # 自分の投稿
        # アンダーバー2つで逆参照のモデルの属性を文字列で取得できる
        my_posts = Post.objects.filter(post_user__username=username, created_date__lte=timezone.now()).order_by('-created_date')
        my_posts_count = len(my_posts)
        context['my_posts'] = my_posts
        context['my_posts_count'] = my_posts_count

        if username is not context['user'].username:
            result = Connection.objects.filter(follower__username=context['user'].username).filter(following__username=username)
            context['connected'] = True if result else False

            con_login_following = Connection.objects.filter(follower__username=context['user'])
            context['login_following_username'] = [f'{user.following}' for user in con_login_following]


        return context

class FollowingList(ProfileDetail, LoginRequiredMixin):
    template_name = 'butter/following_list.html'

class FollowerList(ProfileDetail, LoginRequiredMixin):
    template_name = 'butter/follower_list.html'

class UserUpdateView(UpdateView, LoginRequiredMixin):
    template_name = 'butter/edit_profile.html'
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user

    # reverse_lazyで引数とキーワード引数を返す
    def get_success_url(self):
        return reverse_lazy('edit_profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile has been changed')
        return super().form_valid(form)


class Login(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'registration/login.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class PasswordChange(PasswordChangeView, LoginRequiredMixin):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change')
    template_name = 'registration/password_change.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Password has been changed')
        return super().form_valid(form)
        


class PasswordChangeDone(PasswordChangeDoneView, LoginRequiredMixin):
    template_name = 'registration/password_changed_done.html'


# # フォロー
@login_required
def follow_view(request, *args, **kwargs):

    try:
        #request.user.username = ログインユーザーのユーザー名を渡す。
        follower = MyUser.objects.get(username=request.user.username)
# 　　　　 kwargs['username'] = フォロー対象のユーザー名を渡す。
        following = MyUser.objects.get(username=kwargs['username'])
    #例外処理：もしフォロー対象が存在しない場合、警告文を表示させる。
    except MyUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('home'))
# 　　フォローしようとしている対象が自分の場合、警告文を表示させる。
    if follower == following:
        messages.warning(request, '自分自身はフォローできません')
    else:
        #フォロー対象をまだフォローしていなければ、DBにフォロワー(自分)×フォロー(相手)という組み合わせで登録する。
        #createdにはTrueが入る
        _, created = Connection.objects.get_or_create(follower=follower, following=following)

# 　　　　 もしcreatedがTrueの場合、フォロー完了のメッセージを表示させる。
        if (created):
            messages.success(request, '{}をフォローしました'.format(following.username))
        #既にフォロー相手をフォローしていた場合、createdにはFalseが入る。
        #フォロー済みのメッセージを表示させる。
        else:
            messages.warning(request, 'すでに{}をフォローしています'.format(following.username))

    # return HttpResponseRedirect(reverse_lazy('profile', kwargs={'username': following.username}))
    return redirect(request.META['HTTP_REFERER'])

"""フォロー解除"""
@login_required
def unfollow_view(request, *args, **kwargs):

    try:
        follower = MyUser.objects.get(username=request.user.username)
        following = MyUser.objects.get(username=kwargs['username'])
        if follower == following:
            messages.warning(request, '自分自身のフォローを外せません')
        else:
            unfollow = Connection.objects.get(follower=follower, following=following)
            #フォロワー(自分)×フォロー(相手)という組み合わせを削除する。
            unfollow.delete()
            messages.success(request, '{}のフォローを外しました'.format(following.username))
    except MyUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('home'))
    except Connection.DoesNotExist:
        messages.warning(request, '{0}をフォローしませんでした'.format(following.username))

    # return HttpResponseRedirect(reverse_lazy('profile', kwargs={'username': following.username}))

    return redirect(request.META['HTTP_REFERER'])


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_user = request.user
            post.created_date = datetime.now()
            post.save()
            return redirect('home')
    else:
        form = PostForm()
        
    return render(request, 'butter/post_new.html', {'form': form})