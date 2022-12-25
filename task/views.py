from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy

from task.forms import (
    TaskTypeForm,
    TaskForm,
    TaskSearchForm,
    TaskTypeSearchForm,
)
from task.models import Task, TaskType


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related("task_type")
    paginate_by = 8
    template_name = "task/task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        searched_task = self.request.GET.get("searched_task", "")
        is_completed = self.request.GET.get("searched_complete_status", "")

        context["search_form"] = TaskSearchForm(
            initial={
                "searched_task": searched_task,
                "searched_complete_status": is_completed,
            }
        )

        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)
        queryset = self.queryset

        if form.is_valid():
            task_type_name = Q(
                task_type__name__icontains=form.cleaned_data["searched_task"]
            )
            is_completed = form.cleaned_data["searched_complete_status"]
            queryset = queryset.filter(
                Q(name__icontains=form.cleaned_data["searched_task"])
                | task_type_name
            )

            if is_completed:
                queryset = queryset.filter(is_completed=False)

        return queryset.distinct()


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    fields = (
        "task_type",
        "name",
        "priority",
        "deadline",
        "description",
        "assignees",
    )
    template_name = "task/task_detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task/task_form.html"
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task/task_form.html"
    success_url = reverse_lazy("task:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task/task_form.html"
    success_url = reverse_lazy("task:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    queryset = TaskType.objects.all()
    paginate_by = 8
    template_name = "task/task_type_list.html"
    context_object_name = "task_type_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)

        task_type_name = self.request.GET.get("searched_task_type", "")

        context["search_form"] = TaskTypeSearchForm(
            initial={"searched_task_type": task_type_name}
        )

        return context

    def get_queryset(self):
        form = TaskTypeSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["searched_task_type"]
            )


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    template_name = "task/task_type_form.html"
    success_url = reverse_lazy("task:task-type-list")
    form_class = TaskTypeForm


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "task/task_type_form.html"
    success_url = reverse_lazy("task:task-type-list")
    context_object_name = "task_type"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task/task_type_form.html"
    success_url = reverse_lazy("task:task-type-list")
    context_object_name = "task_type"


@login_required
def toggle_assign_task(request, pk):
    worker = get_user_model().objects.get(id=request.user.id)
    task = Task.objects.get(id=pk)

    if task in worker.tasks.all():
        worker.tasks.remove(task)
    else:
        worker.tasks.add(task)

    return HttpResponseRedirect(reverse_lazy("task:task-list"))


@login_required
def toggle_perform_task(request, pk):
    task = Task.objects.get(id=pk)

    if not task.is_completed:
        task.is_completed = True
        task.save()

    return HttpResponseRedirect(reverse_lazy("task:task-list"))
