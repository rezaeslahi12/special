from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Post,Comment,Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from . forms import PostCreateUpdateForm,CommentCreateForm,ReplyCommentForm,SearchPostForm
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
class HomeView (View):
    template_name = 'home/index.html'
    form_class = SearchPostForm
    def get(self,request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])

        return render(request,self.template_name,{'posts':posts , 'form':self.form_class})
class PostDetailView(View):
    form_class = CommentCreateForm
    template_name ='home/detail.html'
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs['id'] , slug = kwargs['slug'])
        return super().setup(request, *args, **kwargs)
    def get(self,request,*args,**kwargs):
        comments = self.post_instance.pcomment.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_instance.post_can_like(request.user):
            can_like = True
        return render(request,self.template_name,{'post': self.post_instance , 'comments':comments ,
                                                         'form':self.form_class ,'can_like':can_like})

    @method_decorator(login_required)
    def post(self,request,*args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request,'you commented successfully' ,'success')
            return redirect('home:PostDetail',self.post_instance.id,self.post_instance.slug)

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = get_object_or_404(Post,pk = post_id)
        if post.user.id  == request.user.id:
            post.delete()
            messages.success(request,'Post Deleted Successfully','success')
        else:
            messages.error(request,'You Cant Deleted This Post','warning')
        return redirect('home:home')
class PostUpdateView(LoginRequiredMixin,View):
    template_name = 'home/update.html'
    form_class = PostCreateUpdateForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])

        return super().setup(request,*args,**kwargs)


    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance

        if not request.user.id == post.user.id:
            messages.error(request,'You Cant Update This Post','warning')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)
    def get(self,request,post_id):
        post =self.post_instance

        form = self.form_class(instance=post)
        return render(request,self.template_name,{'form' : form})

    def post(self,request,post_id):
        post =self.post_instance
        form = self.form_class(request.POST,request.FILES, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30],allow_unicode = True)
            new_post.save()
            messages.success(request,'your posted updated successfully')
            return redirect('home:PostDetail',post.id , post.slug)
class PostCreateView(LoginRequiredMixin,View):
    template_name =  'home/create.html'
    form_class = PostCreateUpdateForm
    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form': form})
    def post(self,request):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30],allow_unicode = True)
            new_post.user = request.user
            new_post.save()
            messages.success(request,'your posted created successfully')
            return redirect('home:PostDetail',new_post.id,new_post.slug)
        return render(request,self.template_name,{'form' : self.form_class})


class ReplyCommentView(View):
    form_class = ReplyCommentForm
    def post(self,request,post_id,comment_id):
        post = get_object_or_404(Post,pk=post_id)
        comment = get_object_or_404(Comment,pk =comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request,'Yor Reply Submitted','success')
        return redirect('home:PostDetail',post.id,post.slug)

class PostLikeView(LoginRequiredMixin,View):
    def get (self,request,post_id):
        post = get_object_or_404(Post,pk = post_id)

        like = Vote.objects.filter(post = post , user = request.user)
        if like.exists():
            messages.error(request,'You already liked it','danger')
        else:
            Vote.objects.create(user=request.user , post = post)
            messages.success(request,'you liked successfully','success')
        return redirect('home:PostDetail' , post.id , post.slug)



