from django.shortcuts import render
from proforma.models import Proforma
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Requestion

# Create your views here.
def requestiondetail(request):
     return render(request, "requestion/requestion_detail.html")


class RequestionList(LoginRequiredMixin, ListView):
    model = Requestion
    context_object_name = 'reqs'

class ProformaSubmit(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Proforma
    fields = ['requestion', 'user', 'price']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def clean_password(self):
        data = self.cleaned_data['price']
        return data
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
    