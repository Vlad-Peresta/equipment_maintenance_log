from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views import generic
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import (
    LoginForm,
    SignUpForm,
    WorkerUpdateForm,
    WorkerSearchForm,
)


def login_view(request):
    form = LoginForm(request.POST or None)
    message = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy("log:index"))
            else:
                message = "Invalid credentials"
        else:
            message = "Error validating the form"

    return render(
        request, "registration/login.html", {"form": form, "message": message}
    )


def register_worker(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse_lazy("log:index"))
    else:
        form = SignUpForm()

    return render(request, "registration/register.html", {"form": form})


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    queryset = get_user_model().objects.select_related("position")
    paginate_by = 8
    template_name = "worker/worker_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        searched_worker = self.request.GET.get("searched_worker", "")
        context["search_form"] = WorkerSearchForm(
            initial={"searched_worker": searched_worker}
        )

        return context

    def get_queryset(self):
        form = WorkerSearchForm(self.request.GET)
        queryset = self.queryset

        if form.is_valid():
            queryset = queryset.filter(
                Q(first_name__icontains=form.cleaned_data["searched_worker"])
                | Q(last_name__icontains=form.cleaned_data["searched_worker"])
                | Q(username__icontains=form.cleaned_data["searched_worker"])
            )

        return queryset.distinct()


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "worker/worker_detail.html"


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("worker:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("worker:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("worker:worker-list")
    template_name = "worker/worker_detail.html"
