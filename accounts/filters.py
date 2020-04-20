import django_filters
from .models import *
from .forms import *
from django import forms
from datetime import datetime
from django.contrib.auth.models import User

class TransactionDetailsFilter(django_filters.FilterSet):
    
    transaction__transact_date = django_filters.DateFilter(field_name='transaction__transact_date', lookup_expr='iexact', label='Transaction Date', widget=forms.TextInput(attrs={'type': 'date'}))
    transactDet_desc = django_filters.CharFilter(field_name='transactDet_desc', lookup_expr='icontains', label='Transaction Desc.')
    transaction__owner = django_filters.ModelChoiceFilter(field_name='transaction__owner', lookup_expr='username__iexact', label='Transaction Owner', queryset=User.objects.select_related().filter(profile__role=1) | User.objects.select_related().filter(profile__role=2))
    transaction__creator = django_filters.ModelChoiceFilter(field_name='transaction__creator', lookup_expr='username__iexact', label='Transaction Creator', queryset=User.objects.select_related().filter(profile__role=3))

    class Meta:
        
        model = TransactionDetails
        form = FilterForm
        fields = ['transaction__transact_date', 'transactDet_desc', 'transaction__owner', 'transaction__creator']

class MonthlyReportFilter(django_filters.FilterSet):
    # widget=forms.TextInput(attrs={'type': 'month'})
    transaction__transact_date = django_filters.DateFromToRangeFilter(field_name='transaction__transact_date', label='Transaction Date', widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))
    transaction__owner = django_filters.ModelChoiceFilter(field_name='transaction__owner', lookup_expr='username__iexact', label='Transaction Owner', queryset=User.objects.select_related().filter(profile__role=1) | User.objects.select_related().filter(profile__role=2))
    # date_range = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))
    class Meta:
        
        model = TransactionDetails
        form = MonthlyReportForm
        fields = ['transaction__transact_date', 'transaction__owner', 'date_range']