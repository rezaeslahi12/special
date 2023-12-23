from django.urls import path,re_path
from . import views

app_name = 'home'
urlpatterns = [
    path('' , views.HomeView.as_view(),name='home'),
    re_path(r'^post/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='PostDetail'),

    # path('post/<int:post_id>/<slug:post_slug>/',views.PostDetailView.as_view(),name = 'PostDetail'),
    path('post/delete/<int:post_id>/',views.PostDeleteView.as_view(),name = 'PostDelete'),
    # re_path(r'^post/update/(?P<id>\d+)/$', views.PostUpdateView.as_view(), name='PostUpdate'),

    path('post/update/<int:post_id>/',views.PostUpdateView.as_view(),name = 'PostUpdate'),
    path('post/create/',views.PostCreateView.as_view(),name = 'PostCreate'),
    path('reply/<int:post_id>/<int:comment_id>/',views.ReplyCommentView.as_view(),name = 'ReplyComment'),
    path('like/<int:post_id>/',views.PostLikeView.as_view(),name = 'PostLike'),

]