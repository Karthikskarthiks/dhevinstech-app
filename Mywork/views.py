from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from .models import Labour, Site, WorkDetail
from .serializers import LabourSerializer, SiteSerializer, WorkDetailSerializer
from .forms import WorkDetailForm


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
    workdetails = WorkDetail.objects.select_related('vendor', 'site').prefetch_related('labours')

    # Filters
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