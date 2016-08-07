from django.conf.urls import include, url
from . import views
from .views import BlogListView, ArticleDetailView

urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blog_list'),
    url(r'^blog/(?P<cid>\d+)/$', BlogListView.as_view(), name='view_blog'),
    url(r'^article/(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='view_article'),
]
