from django.urls import path, include
from . import views
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required

app_name = 'accounts'

urlpatterns = [
    path('', login_required(views.SearchView.as_view()), name='transaction_search'),
    path('report', login_required(views.MonthlyReportView.as_view()), name='transaction_report'),
	path('record/<int:pk>/', login_required(views.TransactionDetailView.as_view()), name='transaction_detail'),
    path('record/create/', login_required(views.TransactionCreate.as_view()), name='transaction_create'),
    path('record/update/<int:pk>/', login_required(views.TransactionUpdate.as_view()), name='transaction_update'),
    path('record/delete/<int:pk>/', login_required(views.TransactionDelete.as_view()), name='transaction_delete'),
]
