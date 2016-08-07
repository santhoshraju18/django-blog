from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Category, Article
import random

class ReadNextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ReadNextMixin, self).get_context_data(**kwargs)
        context['article_next_list'] = Article.objects.order_by('?')[:4]
        context['category_list'] = get_list_or_404(Category)
        return context

class BlogListView(ReadNextMixin, ListView):

    model = Category
    template_name = 'blog/category_list.html'  

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        random_idx = random.randint(0, Article.objects.count() - 1)
        context['article_object'] = Article.objects.all()[random_idx]
        if 'cid' in self.kwargs:
			category = get_object_or_404(Category, id=self.kwargs['cid'])
			context['category_data'] = category
			context['article_list'] = Article.objects.filter(category=category.id)
        else:
        	context['article_list'] = get_list_or_404(Article)
    	return context


class ArticleDetailView(ReadNextMixin, DetailView):

    model = Article
    template_name = 'blog/article_detail.html'  
