from django.shortcuts import render
from proforma.models import Proforma
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Requestion
from django.utils import timezone
from django.contrib.auth.models import User
from proforma.models import Proforma


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


# Create your views here.
def requestiondetail(request):
     
    return render(request, "requestion/requestion_detail.html")


class RequestionList(LoginRequiredMixin, ListView):
    model = Requestion
    context_object_name = 'reqs'
    paginate_by = 2


class RequestionDetails(LoginRequiredMixin, DetailView):
    model = Requestion
    context_object_name = "objs"
    template_name = 'requestion/requestion_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RequestionDetails, self).get_context_data(**kwargs)
        print(context['objs'].expirey_date)
        if context['objs'].expirey_date > timezone.now():
            context['expired'] = False
        else:
            context['expired'] = True
        return context



class ExpiredRequestionDetails(SuperUserRequiredMixin, DetailView):
    model = Requestion
    context_object_name = "objs"
    template_name = 'requestion/requestion_detail_expired.html'
    def get_context_data(self, **kwargs):
        context = super(ExpiredRequestionDetails, self).get_context_data(**kwargs)
        proformas = Proforma.objects.filter(requestion=context['objs'].id).all()
        # prolist = []
        # for pro in proformas:
        #     if pro.price
        #     prolist = pro
        #     pro.price = int(pro.price)
        #     print(int(pro.price))

        context['proformas'] = proformas

        return context