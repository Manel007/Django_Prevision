from django.shortcuts import render, get_object_or_404, redirect
from .models import CropYield
from .forms import YieldForm

# List all yields
def yield_list(request):
    yields = CropYield.objects.all()
    return render(request, 'agriculture/yield_list.html', {'yields': yields})

# Yield details
def yield_detail(request, pk):
    yield_item = get_object_or_404(CropYield, pk=pk)  # Corrected model name
    return render(request, 'agriculture/yield_detail.html', {'yield': yield_item})

# Create new yield
def yield_create(request):
    if request.method == "POST":
        form = YieldForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('yield_list')
    else:
        form = YieldForm()
    return render(request, 'agriculture/yield_form.html', {'form': form})

# Update a yield
def yield_update(request, pk):
    yield_item = get_object_or_404(CropYield, pk=pk)  # Corrected model name
    if request.method == "POST":
        form = YieldForm(request.POST, instance=yield_item)
        if form.is_valid():
            form.save()
            return redirect('yield_list')
    else:
        form = YieldForm(instance=yield_item)
    return render(request, 'agriculture/yield_form.html', {'form': form})

# Delete a yield
def yield_delete(request, pk):
    yield_item = get_object_or_404(CropYield, pk=pk)  # Corrected model name
    if request.method == "POST":
        yield_item.delete()
        return redirect('yield_list')
    return render(request, 'agriculture/yield_confirm_delete.html', {'yield': yield_item})
