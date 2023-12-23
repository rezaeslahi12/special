from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('profile/<int:user_id>/',views.UserProfileView.as_view(),name='profile'),
    path('reset/',views.ResetPasswordView.as_view(),name = 'reset_password'),
    path('reset/done/',views.UserPasswordResetDoneView.as_view(),name = 'password_reset_done'),
    path('confrim/<uidb64>/<token>/',views.UserPasswordResetConfrimView.as_view(),name='password_reset_confirm'),
    path('confrim/complete/',views.UserPasswordResetCompleteView.as_view(),name = 'password_reset_complete'),
    path('follow/<int:user_id>/',views.UserFollowView.as_view(),name = 'user_follow'),
    path('unfollow/<int:user_id>/',views.UserUnFollowView.as_view(),name = 'user_Unfollow'),
    path('edit_user/',views.UserEditView.as_view(),name  = 'edit_user'),
]