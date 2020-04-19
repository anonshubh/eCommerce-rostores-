from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from products.models import Product

class SearchProductView(ListView):
    model = Product
    template_name='search/view.html'

    def get_context_data(self,*args,**kwargs):
        context = super(SearchProductView,self).get_context_data(*args,**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
    
    def get_queryset(self,*args,**kwargs):
        query = self.request.GET.get('q',None)
        if query == '':
            query=None
        if query is not None:
            lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(price__iexact=query) | Q(tag__title__icontains=query)
            return Product.objects.filter(lookups).distinct()
        return Product.objects.filter(featured=True)
