from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_tables2.config import RequestConfig
from crispy_forms.layout import Button, Reset, Submit
from crispy_forms.layout import HTML as crispy_HTML
from .models import Profile
from django.db.models import Q
from calendar import monthrange
from datetime import date

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

# ##########################################################################
# #                           Generate pdf                             #
# ##########################################################################

# https://gist.github.com/pikhovkin/5642563
# https://github.com/Kozea/WeasyPrint/issues/92
def generate_receipt(request, pk):
    trans_dets = get_object_or_404(TransactionDetails, pk=pk)
    date_str = date.today().strftime("%d-%m-%Y")
    trans_date_str = trans_dets.transaction.transact_date.strftime("%Y%m%d")
    template = loader.get_template('accounts/receipt.html')
    
    role_int = trans_dets.transaction.owner.profile.role
    role = ''
    if role_int == 1:
        role = 'Bhante'
    elif role_int == 2:
        role = 'Sayalay'
    
    context = {
        'name': role + ' ' + trans_dets.transaction.owner.username,
        'amount': trans_dets.rm,
        'date': date_str,
        'filename': 'ref_{}_{}_{}'.format(trans_date_str,  trans_dets.transaction.transact_id, trans_dets.transactDet_id),
    }
    return HttpResponse(template.render(context, request))

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
#                           Monthly report views                             #
##########################################################################

class MonthlyReportView(ListView):
    template_name = 'accounts/monthly_report.html'
    def get(self, request):
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
        date_str = date.today().strftime("%d-%m-%Y")

        return render(request, self.template_name, {
            'filter': transactionDetails_filter,
            'table': result_table,
            'date': date_str,
        })
