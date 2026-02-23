from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from .models import Labour, Site, WorkDetail
from .serializers import LabourSerializer, SiteSerializer, WorkDetailSerializer
from .forms import WorkDetailForm
from django.http import HttpResponse


def home(request):
    return HttpResponse("WorkFlowProject is live!")


# --- API ViewSets ---
class LabourViewSet(viewsets.ModelViewSet):
    queryset = Labour.objects.all()
    serializer_class = LabourSerializer
    
class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class WorkDetailViewSet(viewsets.ModelViewSet):
    queryset = WorkDetail.objects.all()
    serializer_class = WorkDetailSerializer

# --- Template Views ---
def workdetail_list(request):
    workdetails = WorkDetail.objects.all()
    return render(request, 'workdetail_list.html', {'workdetails': workdetails})
def add_workdetail(request):
    if request.method == 'POST':
        form = WorkDetailForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.save()
            form.save_m2m()   
            return redirect('workdetail_list')
    else:
        form = WorkDetailForm()

    return render(request, 'add_workdetail.html', {'form': form})

def delete_workdetail(request, pk):
    wd = get_object_or_404(WorkDetail, pk=pk)
    wd.delete()
    return redirect('workdetail_list')
