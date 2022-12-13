from django.views import generic
from .models import Sales


class DELETEVIEW(generic.DeleteView):
    model = Sales
    template_name = 'sales/main.html'
    context_object_name = 'qs'


class DELETEVIEW(generic.DeleteView):
    model = Sales
    template_name = 'sales/detail.html'
