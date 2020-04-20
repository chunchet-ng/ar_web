from celery import shared_task
from .models import Invoice
from django.db.models import Q
from datetime import date
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def update_status():
    criterion1 = ~Q(invoice_status__exact="Completed")
    invoice_list = Invoice.objects.filter(criterion1)
    for invoice in invoice_list:
        new_status = ''
        if invoice.due_date == date.today():
            new_status = 'Due'
        elif invoice.due_date < date.today():
            new_status = 'Overdue'
        elif invoice.due_date > date.today():
            new_status = 'Pending'

        if new_status != invoice.invoice_status:
            old_status = invoice.invoice_status
            invoice.invoice_status = new_status
            invoice.save()
            logger.info('Invoice {} changed from {} to {}.'.format(invoice.invoice_id, old_status, invoice.invoice_status))
        else:
            continue