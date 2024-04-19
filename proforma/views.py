from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core import signing
from .models import Post, Proforma
from requestion.models import Requestion
from django.utils import timezone


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser

def home(request):
    blog = Post.objects.all().order_by("-date_posted")
    context = {
         "blogs": blog[:3]
    }
    return render(request, "proforma/home.html", context)



def about(request):
     return render(request, "proforma/about.html")

def blog(request):
     return render(request, "proforma/blog_list.html")

def blogdetail(request):
     return render(request, "proforma/blog_detail.html")

class BlogDetail(DetailView):
    model = Post
    context_object_name = 'blog'
    template_name = "proforma/blog_detail.html"

class Home(ListView):
    template_name = 'proforma/blog_list.html'
    model = Post
    ordering = '-date_posted'
    context_object_name = 'blogs'


def notifications_list(request):
    requestions = Requestion.objects.all().order_by("-expirey_date")
    expired_reqs = []

    for requestion in requestions:
        print(type(requestion.expirey_date))
        print("///////")
        if requestion.expirey_date < timezone.now():
            expired_reqs.append(requestion)

    context = { 
        "requestion": expired_reqs
    }


    return render(request, "proforma/notifications_list.html", context)

class Notifications_list(SuperUserRequiredMixin, TemplateView):
    template_name = "proforma/notifications_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requestions = Requestion.objects.all().order_by("-expirey_date")
        expired_reqs = []

        for requestion in requestions:
            print(type(requestion.expirey_date))
            print("///////")
            if requestion.expirey_date < timezone.now():
                expired_reqs.append(requestion)

        context["requestion"] = expired_reqs
        context["is_super"] = self.request.user.is_superuser
        return context


class ProformaSubmit(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Proforma
    fields = ['price']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.requestion = Requestion.objects.get(pk=int(self.request.GET.get('id')))
        return super().form_valid(form)
    
    def save(self, form, *args, **kwargs):
        data = form.cleaned_data['price']
        self.price = data
        super().save(*args, **kwargs)