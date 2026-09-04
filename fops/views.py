from django.shortcuts import render, redirect
from fops.forms import FopForm
from fops.models import Fops


def fop_list(request):
    fops = Fops.created_at
    return render(request, 'fops/fop_list.html', {'fops': fops})

def fop_create(request):
    if request.method == 'POST':
        form = FopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fop_list')
    else:
        form = FopForm()

    return render(request, 'fops/fop_form.html', {'form': form})
