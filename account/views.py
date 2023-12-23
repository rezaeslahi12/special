from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import UserRegistrationForm,UserLoginForm,UserEditForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . models import Relation

class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)
    def get (self,request):
        form = self.form_class
        return render(request,self.template_name,{'form' : form})
    def post (self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password1'])
            messages.success(request,'You Successfully Register','success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    form_class=UserLoginForm
    template_name = 'account/login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form' : form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username = cd['username'] , password = cd['password'])
            if user:
                login(request,user)
                messages.success(request,'you Successfully Login','success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request,'UserName Or Your Password is Wrong','warning')
        return render(request,self.template_name,{'form': form})


class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'you Successfully logout','success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = get_object_or_404(User,pk=user_id)
        post = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_follower = True

        else:
            is_follower = False


        return render(request,'account/profile.html',{'user':user,'post':post,'is_follower':is_follower})
class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = ('account/password_reset_email.html')

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'
class UserPasswordResetConfrimView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'



class UserFollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists():
            messages.error(request,'You are following this user','danger')
        else:
            Relation(from_user=request.user , to_user=user).save()
            messages.success(request,'You have successfully followed','success')
        return redirect('account:profile',user_id)

class UserUnFollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'You have successfully Unfollowed', 'success')
        else:
            messages.error(request,'You are not following this user','danger')
        return redirect('account:profile',user_id)


class UserEditView(LoginRequiredMixin,View):
    form_class = UserEditForm

    def get (self,request):
        form = self.form_class(instance=request.user.profile,initial={'email':request.user.email})
        return render(request,'account/edit_user.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST , instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request,'Profile Edited Successfully','success')
        return redirect('account:profile',request.user.id)















