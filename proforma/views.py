from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.utils import timezone

#Required models for proforma views and landing page
from .models import Post, Proforma
from users.models import BusinessInfo
from requestion.models import Requestion
from projects.models import Project


from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')



class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser

def home(request):
    project = Project.objects.all().order_by("-updated_at")
    context = {
         "projects": project[:3]
    }
    return render(request, "proforma/home.html", context)



def about(request):
     context = {
         'title': "About"
     }
     return render(request, "proforma/about.html", context=context)

def blog(request): 
     return render(request, "proforma/blog_list.html")

def blogdetail(request):
     return render(request, "proforma/blog_detail.html")

class BlogDetail(DetailView):
    model = Post
    context_object_name = 'blog'
    template_name = "proforma/blog_detail.html"

class BlogList(ListView):
    template_name = 'proforma/blog_list.html'
    model = Post
    context_object_name = 'blogs'
    ordering = ['-updated_at'] 
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Blog List"

        return context

def notifications_list(request):
    requestions = Requestion.objects.all().order_by("-expirey_date")
    expired_reqs = []

    for requestion in requestions:
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
            if requestion.expirey_date < timezone.now():
                expired_reqs.append(requestion)

        paginator = Paginator(expired_reqs, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['title'] = 'Notification'
        context["page_obj"] = page_obj
        context['is_paginated'] = True
        context["is_super"] = self.request.user.is_superuser
        return context


class Users_Notification_list(LoginRequiredMixin, TemplateView):
    template_name = "proforma/user_notifications_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        userproformas = user.proformas.all().order_by('-updated_at')
        paginator = Paginator(userproformas, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        context['title'] = 'Notification'
        context["is_super"] = self.request.user.is_superuser
        context['is_paginated'] = True
        return context


class ProformaSubmit(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Proforma
    fields = ['price', 'business', 'additional_infos']
    context_object_name = "objs"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter the queryset for the 'business' field to only include businesses related to the current user
        form.fields['business'].queryset = BusinessInfo.objects.filter(user=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        business = BusinessInfo.objects.filter(user=user)
        if business.exists():
            context['nobusiness'] = False
        else:
            context['nobusiness'] = True
            messages.warning(self.request, 'You should add a business license before submitting a proforma')
        return context

    def form_valid(self, form):
        user = self.request.user
        business = form.cleaned_data['business']
        requestion_id = self.request.GET.get('id')
        requestion = get_object_or_404(Requestion, pk=requestion_id)
        
        # Check if the user has already submitted a proforma with the same business
        if Proforma.objects.filter(user=user, business=business, requestion=requestion).exists():
            messages.warning(self.request, 'A user cannot apply twice with the same business license')
            return redirect('Blog')  # Replace 'previous_page' with the appropriate URL name

        # Set the user and requestion for the proforma
        form.instance.user = user
        form.instance.requestion = requestion
        messages.success(self.request, 'You have successfully submitted the proforma and you can check it in your Notification page')
        return super().form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        if context['nobusiness']:
            return redirect('newbusiness')
        return super().render_to_response(context, **response_kwargs)