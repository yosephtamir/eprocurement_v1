import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.shortcuts import render
from proforma.models import Proforma
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Requestion
from django.utils import timezone
from proforma.models import Proforma
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa #Used for rendering the view to pdf
from io import BytesIO
from django.db.models import Q #used for filtering in or maner




class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    '''This is used to identify whether the user is a super user or not'''
    def test_func(self):
        return self.request.user.is_superuser



class RequestionList(LoginRequiredMixin, ListView):
    """Lists all available active requestions/proformas"""
    model = Requestion
    context_object_name = 'reqs'
    paginate_by = 12
    ordering = ['-created_at']

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        requestions = Requestion.objects.all()
        if search_query:
            requestions = requestions.filter(
                Q(title__icontains=search_query) |
                Q(details__icontains=search_query) |
                Q(subcategory__name__icontains=search_query) |
                Q(subcategory__category__name__icontains=search_query)
            )
        return requestions.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        if not self.get_queryset():
            messages.warning(self.request, f'Sorry Requests not found for "{search_query}"')
        else:
            context['q'] = True
        context['search_query'] = search_query 
        return context

class RequestionDetails(LoginRequiredMixin, DetailView):
    '''Detailed view of a single active Request'''
    model = Requestion
    context_object_name = "objs"
    template_name = 'requestion/requestion_detail.html'

    def get_context_data(self, **kwargs):
        '''This method is used to filter expired requests/proformas'''
        context = super(RequestionDetails, self).get_context_data(**kwargs)
        print(context['objs'].expirey_date)
        if context['objs'].expirey_date > timezone.now():
            context['expired'] = False
        else:
            context['expired'] = True
        return context



class ExpiredRequestionDetails(SuperUserRequiredMixin, DetailView):
    '''This is used to display all expired requests/proformas to the admin user'''
    model = Requestion
    context_object_name = "objs"
    template_name = 'requestion/requestion_detail_expired.html'
    def get_context_data(self, **kwargs):
        '''This method is used to filter all the proforma invoices submitted
           to this single request and sort it by price'''
        context = super(ExpiredRequestionDetails, self).get_context_data(**kwargs) 
        proformas = Proforma.objects.filter(requestion=context['objs'].id).all().values()
        sorted_proformas = sorted(proformas, key=lambda i: i['price'])
        context['proformas'] = sorted_proformas

        return context

class FiledRequestionDetails(LoginRequiredMixin, DetailView):
    '''Filed Requestion detailed view'''
    model = Requestion
    context_object_name = "objs"
    template_name = 'requestion/requestion_detail_expired.html'
    def get_context_data(self, **kwargs):
        '''This method is used to view the proforma invoices submitted
           to this single request'''
        context = super(FiledRequestionDetails, self).get_context_data(**kwargs)
        user = self.request.user
        userproformas = user.proformas.filter(requestion=context['objs'].id).all()
        context['proformas'] = userproformas

        return context
    
class PrintableRequestionDetails(LoginRequiredMixin, DetailView):
    model = Requestion
    context_object_name = "objs"
    template_name = 'requestion/requestion_printable_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PrintableRequestionDetails, self).get_context_data(**kwargs)
        user = self.request.user
        userproformas = user.proformas.filter(requestion=context['objs'].id).all()
        context['proformas'] = userproformas
        return context

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
        """
        if uri.startswith(settings.MEDIA_URL):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        elif uri.startswith(settings.STATIC_URL):
            path = finders.find(uri.replace(settings.STATIC_URL, ""))
            if path:
                path = os.path.realpath(path)
            else:
                path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (settings.STATIC_URL, settings.MEDIA_URL))
        return path

    def render_to_response(self, context, **response_kwargs):
        template = self.get_template_names()[0]
        html = render_to_string(template, context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=self.link_callback)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse('We had some errors with code %s' % pdf.err, status=400)
