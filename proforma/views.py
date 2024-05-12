from django.shortcuts import render, redirect, get_object_or_404
from requestion.models import Requestion
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core import signing
from .models import Post, Proforma
from users.models import BusinessInfo
from requestion.models import Requestion
from django.utils import timezone

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')


from django.contrib import messages


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
    paginate_by = 2


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
    fields = ['price', 'business']
    context_object_name = "objs"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter the queryset for the 'business' field to only include businesses related to the current user
        form.fields['business'].queryset = BusinessInfo.objects.filter(user=self.request.user)
        print(form.fields['business'])
        return form

    def get_context_data(self, **kwargs):
        context = super(ProformaSubmit, self).get_context_data(**kwargs)
        user = self.request.user
        business = BusinessInfo.objects.filter(user=user).all()
        print(business)

        if business:
            context['nobusiness'] = False
        else:
            context['nobusiness'] = True
            messages.warning(self.request,'You should add a business licence before submitting a proforma')
        return context
            

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.requestion = get_object_or_404(Requestion, pk=int(self.request.GET.get('id')))
        return super().form_valid(form)
    
    def save(self, form, *args, **kwargs):
        data = form.cleaned_data['price']
        self.price = data
        super().save(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if context['nobusiness']:
            return redirect('newbusiness')
        return super(ProformaSubmit, self).render_to_response(context, **response_kwargs)