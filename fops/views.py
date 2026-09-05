from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Fops
from .forms import FopsForm


def fop_list_view(request):
    """Відображення списку всіх ФОПів"""
    fops = Fops.objects.all().order_by('-created_at')
    return render(request, 'fops/fop_list.html', {'fops': fops})


def fop_create_view(request):
    """Створення нового ФОПа"""
    if request.method == 'POST':
        form = FopsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ФОП успішно зареєстрований!")
            return redirect('fops:list')
    else:
        form = FopsForm()
    return render(request, 'fops/fop_form.html', {'form': form, 'title': 'Реєстрація нового ФОП'})


def fop_update_view(request, pk):
    """Редагування реквізитів ФОПа"""
    fop = get_object_or_404(Fops, pk=pk)
    if request.method == 'POST':
        form = FopsForm(request.POST, instance=fop)
        if form.is_valid():
            form.save()
            messages.success(request, f"Реквізити ФОП {fop.full_name} успішно оновлено!")
            return redirect('fops:list')
    else:
        form = FopsForm(instance=fop)
    return render(request, 'fops/fop_form.html', {'form': form, 'title': 'Редагування реквізитів ФОП', 'fop': fop})


