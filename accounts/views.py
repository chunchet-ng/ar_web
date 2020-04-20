from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_tables2.config import RequestConfig
from crispy_forms.layout import Button, Reset, Submit
from crispy_forms.layout import HTML as crispy_HTML
from .pdf import PdfGenerator
from .models import Profile
from django.db.models import Q
from calendar import monthrange
from datetime import date
from .utils import int2words

from .tables import *
from .models import *
from .forms import *
from .filters import *
##########################################################################
#                           Invoice views                             #
##########################################################################

#modified from https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6
#repo https://github.com/zxenia/example-inline-formsets

class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'accounts/transaction_detail.html'

    def get_context_data(self, **kwargs):
        # qs = Product.objects.filter(invoice__invoice_id__iexact = self.object.invoice_id).select_related('invoice')
        qs = TransactionDetails.objects.filter(transaction__transact_id__iexact = self.object.transact_id)
        table = TransactionDetailTable(qs)
        context = super(TransactionDetailView, self).get_context_data(**kwargs)
        context['table'] = table
        return context

class TransactionCreate(CreateView):
    model = Transaction
    template_name = 'accounts/transaction_create.html'
    form_class = TransactionForm

    def get_context_data(self, **kwargs):
        data = super(TransactionCreate, self).get_context_data(**kwargs)
        data['title'] = 'Transaction Form'
        if self.request.POST:
            data['transactions'] = TransactionDetailsFormSet(self.request.POST)
        else:
            data['transactions'] = TransactionDetailsFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        transactions = context['transactions']
        with transaction.atomic():
            form.instance.creator = self.request.user
            if transactions.is_valid():
                self.object = form.save()
                transactions.instance = self.object
                transactions.save()
                return super(TransactionCreate, self).form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('accounts:transaction_detail', kwargs={'pk': self.object.pk})


class TransactionUpdate(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'accounts/transaction_create.html'

    def get_context_data(self, **kwargs):
        data = super(TransactionUpdate, self).get_context_data(**kwargs)
        data['title'] = 'Update Transactions'
        if self.request.POST:
            data['transactions'] = TransactionDetailsFormSet(self.request.POST, instance=self.object)
        else:
            data['transactions'] = TransactionDetailsFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        transactions = context['transactions']
        with transaction.atomic():
            form.instance.creator = self.request.user
            if transactions.is_valid():
                self.object = form.save()
                transactions.instance = self.object
                transactions.save()
                return super(TransactionUpdate, self).form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('accounts:transaction_detail', kwargs={'pk': self.object.pk})


class TransactionDelete(DeleteView):
    model = Transaction
    template_name = 'accounts/confirm_delete.html'
#     success_url = reverse_lazy('invoices:invoice_search')

# ##########################################################################
# #                           Generate pdf                             #
# ##########################################################################

# # https://gist.github.com/pikhovkin/5642563
# # https://github.com/Kozea/WeasyPrint/issues/92
# def get_invoice(request, pk, pdf_type):
#     invoice = get_object_or_404(Invoice, pk=pk)
#     subtotal_arr, subtotal, total_discounted, total = calc_total(invoice.has_products.all(), invoice.proj_disc)
#     title = ''
#     if pdf_type == 'inv':
#         title = 'Invoice'
#     elif pdf_type == 'do':
#         title = 'Delivery Order'
#     elif pdf_type == 'quot':
#         title = 'Quotation'
#     elif pdf_type == 'so':
#         title = 'Sales Order'
#     else:
#         return HttpResponseNotFound('<h1>Invalid pdf type!</h1>') 

#     manual_ref_arr = []
#     if invoice.manual_ref1:
#         manual_ref_arr.append(invoice.manual_ref1.strip())
#     if invoice.manual_ref2:
#         manual_ref_arr.append(invoice.manual_ref2.strip())

#     html = loader.render_to_string("invoices/invoice_template_v2.html", {
#         'object': invoice,
#         'subtotal_arr': subtotal_arr,
#         'subtotal': subtotal,
#         'total': total,
#         'total_discounted': total_discounted,
#         'today': get_date(),
#         'title': title,
#         'filename': '{}_{}'.format(invoice.invoice_reference, pdf_type),
#         'manual_ref_arr': manual_ref_arr,
#     })
#     # css = CSS(settings.STATIC_ROOT +  '/invoices/css/invoice_v2.css')
#     # pdf_file = HTML(string=html).write_pdf(stylesheets=[css])
#     # response = HttpResponse(pdf_file, content_type='application/pdf')
#     # new_pdf = PdfGenerator(main_html=html, base_url=request.build_absolute_uri())
#     # response = HttpResponse(new_pdf.render_pdf(), content_type="application/pdf")
#     # response['Content-Disposition'] = "inline; filename={invoice_reference}-invoice.pdf".format(
#     #     invoice_reference=invoice.invoice_reference,
#     # )
#     # return response

#     template = loader.get_template('invoices/invoice_template_v2.html')
#     first_part = int(total.split('.')[0])
#     second_part = int(total.split('.')[1])
#     if second_part == 0:
#         total_str = int2words(first_part) + ' malaysian ringgit '
#     else:
#         total_str = int2words(first_part) + ' malaysian ringgit and ' +int2words(second_part)+' cents' 
#     context = {
#         'object': invoice,
#         'subtotal_arr': subtotal_arr,
#         'subtotal': subtotal,
#         'total': total,
#         'total_discounted': total_discounted,
#         'today': get_date(),
#         'title': title,
#         'filename': '{}_{}'.format(invoice.invoice_reference, pdf_type),
#         'manual_ref_arr': manual_ref_arr,
#         'total_str': total_str.title()
#     }
#     return HttpResponse(template.render(context, request))

# def calc_total(products, proj_disc):
#     amount_arr = []
#     subtotal = 0
#     total = 0
#     if len(products) > 0:
#         for product in products:
#             amount = product.product_unit_price * product.product_quantity * (1 - product.product_unit_disc/100)
#             subtotal += amount
#             amount_arr.append(str(round(amount,2)))
        
#         total_discounted = subtotal * (proj_disc/100)
#         total = subtotal - total_discounted
#         return amount_arr, str(round(subtotal,2)), str(round(total_discounted,2)), str(round(total,2))
#     else:
#         return 0

##########################################################################
#                           Search views                             #
##########################################################################

#modified from https://stackoverflow.com/questions/36871987/django-filter-change-default-form-appearance
#good ref https://kuttler.eu/en/post/using-django-tables2-filters-crispy-forms-together/

class SearchView(ListView):
    template_name = 'accounts/search.html'

    def get(self, request):
        transactionDetails_list = TransactionDetails.objects.all()
        transactionDetails_filter = TransactionDetailsFilter(request.GET, queryset=transactionDetails_list)

        #render reset and clear button dynamically
        has_filter = any(field in request.GET for field in set(transactionDetails_filter.get_fields()))
        helper = transactionDetails_filter.form.helper
        if has_filter:
            button_html = crispy_HTML('<a href="{%  url "accounts:transaction_search" %}" class="btn btn-warning">Reset</a>')
            helper.layout[0][1][0].append(button_html)
        else:
            helper.layout[0][1][0].append(Reset('reset', "Clear", css_class='btn btn-warning'))

        #populate result table with pagination
        result_table = TransactionDetailSearchTable(transactionDetails_filter.qs)
        RequestConfig(request, paginate={"per_page": 5}).configure(result_table)

        return render(request, self.template_name, {
            'filter': transactionDetails_filter,
            'table': result_table,
        })

##########################################################################
#                           Sign up views                             #
##########################################################################

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.role = form.cleaned_data.get('role')
            user.save()
            return redirect('accounts:transaction_search')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

##########################################################################
#                           Debt report views                             #
##########################################################################

class MonthlyReportView(ListView):
    template_name = 'accounts/monthly_report.html'
    
    def get(self, request):
        # today = date.today()
        # year = today.year
        # month = today.month
        # criterion1 = Q(transaction__transact_date__month=month)
        # # criterion2 = ~Q(invoice_status__exact="Completed")
        # transactionDetails_list = TransactionDetails.objects.filter(criterion1)
        # transactionDetails_filter = MonthlyReportFilter(request.GET, queryset=transactionDetails_list)
        transactionDetails_list = TransactionDetails.objects.all()
        transactionDetails_filter = MonthlyReportFilter(request.GET, queryset=transactionDetails_list)

        #render reset and clear button dynamically
        has_filter = any(field in request.GET for field in set(transactionDetails_filter.get_fields()))
        helper = transactionDetails_filter.form.helper
        if has_filter:
            button_html = crispy_HTML('<a href="{%  url "accounts:transaction_report" %}" class="btn btn-warning">Reset</a>')
            helper.layout[0][1][0].append(button_html)
        else:
            helper.layout[0][1][0].append(Reset('reset', "Clear", css_class='btn btn-warning'))

        #populate result table with pagination
        result_table = MonthlyReportTable(transactionDetails_filter.qs)
        RequestConfig(request).configure(result_table)

        return render(request, self.template_name, {
            'filter': transactionDetails_filter,
            'table': result_table,
        })
