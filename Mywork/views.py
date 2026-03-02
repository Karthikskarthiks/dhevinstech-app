from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Labour, Site, WorkDetail
from .serializers import LabourSerializer, SiteSerializer, WorkDetailSerializer
from .forms import WorkDetailForm
import csv


# ------------------------------
# DRF API ViewSets
# ------------------------------
class LabourViewSet(viewsets.ModelViewSet):
    queryset = Labour.objects.all()
    serializer_class = LabourSerializer


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class WorkDetailViewSet(viewsets.ModelViewSet):
    queryset = WorkDetail.objects.all()
    serializer_class = WorkDetailSerializer


# ------------------------------
# Template Views
# ------------------------------
def workdetail_list(request):
    """List all workdetails with optional filtering."""
    workdetails = WorkDetail.objects.select_related('vendor', 'site').prefetch_related('labours').order_by('-date', '-created_at')

    # Filters (friendly, partial, case-insensitive)
    date_query = request.GET.get('date', '')
    labour_query = request.GET.get('labour', '')
    vendor_query = request.GET.get('vendor', '')
    site_query = request.GET.get('site', '')

    if date_query:
        workdetails = workdetails.filter(date=date_query)

    if labour_query:
        workdetails = workdetails.filter(labours__name__icontains=labour_query)

    if vendor_query:
        workdetails = workdetails.filter(vendor__name__icontains=vendor_query)

    if site_query:
        workdetails = workdetails.filter(site__site_name__icontains=site_query)

    workdetails = workdetails.distinct()

    context = {
        'workdetails': workdetails,
        'date_query': date_query,
        'labour_query': labour_query,
        'vendor_query': vendor_query,
        'site_query': site_query,
        'is_filtered': any([date_query, labour_query, vendor_query, site_query]),
    }

    return render(request, 'workdetail_list.html', context)


def add_workdetail(request):
    """Add a new WorkDetail."""
    form = WorkDetailForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('workdetail_list')

    return render(request, 'add_workdetail.html', {'form': form, 'action': 'Add'})


def edit_workdetail(request, pk):
    """Edit an existing WorkDetail."""
    work = get_object_or_404(WorkDetail, pk=pk)
    form = WorkDetailForm(request.POST or None, instance=work)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('workdetail_list')

    return render(request, 'add_workdetail.html', {'form': form, 'action': 'Edit'})


def delete_workdetail(request, pk):
    """Delete a WorkDetail."""
    work = get_object_or_404(WorkDetail, pk=pk)
    work.delete()
    return redirect('workdetail_list')


# ------------------------------
# CSV Export (Backup)
# ------------------------------
def export_workdetails_csv(request):
    """Export all WorkDetails to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="workdetails.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date','Labour','Vendor','Site','Work Details','Material','Check In','Check Out'])

    workdetails = WorkDetail.objects.select_related('vendor', 'site').prefetch_related('labours').order_by('-date', '-created_at')

    for wd in workdetails:
        labours = ", ".join([l.name for l in wd.labours.all()])
        vendor = wd.vendor.name if wd.vendor else ''
        site = f"{wd.site.site_name} {wd.site.location}"
        writer.writerow([
            wd.date,
            labours,
            vendor,
            site,
            wd.work_description,
            wd.material_description or '',
            wd.check_in,
            wd.check_out
        ])

    return response