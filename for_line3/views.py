from django.views import generic
from .models import Sales


class SaleListView(generic.ListView):
    model = Sales
    template_name = 'sales/main.html'
    context_object_name = 'qs'


class SaleDetailView(generic.DetailView):
    model = Sales
    template_name = 'sales/detail.html'
