from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateResponseMixin, View
from django.apps import apps

from accounts.forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from accounts.models import Profile

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from article.models import Post, Content

# Create your mixins here
class AuthorMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)
    
class AuthorEditMixin(object):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class AuthorPostMixin(AuthorMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Post
    fields = ['topic', 'title', 'slug', 'overview']
    success_url = reverse_lazy('accounts:user_profile')
    
class AuthorPostEditMixin(AuthorPostMixin, AuthorEditMixin):
    template_name = 'accounts/manage/post/form.html'
    
# Create your views here.
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, user=new_user)
            return redirect('accounts:user_dashboard')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'accounts/registration/signup.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request, 'accounts/manage/user/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
        
@login_required
def user_dashboard(request):
    return render(request, 'accounts/manage/user/dashboard.html')

class UserProfileView(AuthorPostMixin, ListView):
    template_name = 'accounts/manage/user/profile.html'
    permission_required = 'posts.view_post'
    
class PostCreateView(AuthorPostEditMixin, CreateView):
    permission_required = 'posts.add_post'
    
class PostUpdateView(AuthorPostEditMixin, UpdateView):
    permission_required = 'posts.change_post'
    
class PostDeleteView(AuthorPostMixin, DeleteView):
    permission_required = 'posts.delete_post'
    


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'accounts/manage/content/form.html'
    
    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='article', model_name=model_name)
        return None
    
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['author', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)
    
    def dispatch(self, request, post_id, model_name, id=None):
        self.post = get_object_or_404(Post, id=post_id, post__author=request.user)
        self.model = self.get_model(model_name)
        
        if id:
            self.obj = get_object_or_404(self.model, id=id, author=request.user)
        return super().dispatch(request, post_id, model_name, id)
    
    def get(self, request, post_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj })
    
    def post(self, request, post_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            
            if not id:
                Content.objects.create(post=self.post, item=obj)
            return redirect('accounts:user_post_content_list', self.post.id)
        return self.render_to_response({'form':form, 'object': self.obj})
    