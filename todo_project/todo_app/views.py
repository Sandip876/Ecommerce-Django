from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm, TodoDeleteForm



def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo_app/todo_list.html', {'todos': todos})


@login_required
def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.view_count += 1
    todo.save()
    return render(request, 'todo_app/todo_detail.html', {'todo': todo})


@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['creation_code'] == '1234':  # Secret creation code
                todo = form.save(commit=False)
                todo.user = request.user
                todo.save()
                return redirect('todo_list')
            else:
                form.add_error('creation_code', 'Invalid creation code')
    else:
        form = TodoForm()
    return render(request, 'todo_app/todo_form.html', {'form': form})


@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            if form.cleaned_data['creation_code'] == '1234':  # Secret creation code
                form.save()
                return redirect('todo_list')
            else:
                form.add_error('creation_code', 'Invalid creation code')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo_app/todo_form.html', {'form': form})


@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoDeleteForm(request.POST)
        if form.is_valid():
            if str(form.cleaned_data['deletion_key']) == str(todo.deletion_key):
                todo.delete()
                return redirect('todo_list')
            else:
                form.add_error('deletion_key', 'Invalid deletion key')
    else:
        form = TodoDeleteForm()
    return render(request, 'todo_app/todo_confirm_delete.html', {'todo': todo, 'form': form})
