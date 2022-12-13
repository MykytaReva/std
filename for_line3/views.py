from django.views import generic
from .models import Sales


class DELETEVIEW(generic.DeleteView):
    model = Sales
    # def save(self, commit=True):
    #     instance: UserAvatar = super().save(commit=False)
    #     instance.u_id = get_user_model().id
    #     instance.save()
    #     return instance
    template_name = 'sales/main.html'
    context_object_name = 'qs'


class DELETEVIEW(generic.DeleteView):
    model = Sales
    template_name = 'sales/detail.html'
    
        def save(self, commit=True):    
                
        instance: UserAvatar = super().save(commit=False)
        instance.u_id = get_user_model().id
        instance.save()
        return instance
