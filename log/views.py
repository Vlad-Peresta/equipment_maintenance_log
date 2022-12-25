from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from log.forms import (
    BreakdownForm,
    BreakdownTypeForm,
    EquipmentForm,
    EquipmentTypeForm,
    EquipmentTypeSearchForm,
    BreakdownTypeSearchForm,
    BreakdownSearchForm,
    EquipmentSearchForm,
)
from log.models import (
    Breakdown,
    BreakdownType,
    Equipment,
    EquipmentType,
)
from task.models import Task


@login_required
def index(request):
    staff_amount = get_user_model().objects.count()
    equipment_amount = Equipment.objects.count()
    active_tasks_amount = Task.objects.filter(is_completed=False).count()
    active_failures_amount = Breakdown.objects.filter(status="process").count()

    context = {
        "staff_amount": staff_amount,
        "equipment_amount": equipment_amount,
        "active_tasks_amount": active_tasks_amount,
        "active_failures_amount": active_failures_amount,
    }

    return render(request, "log/index.html", context=context)


class BreakdownListView(LoginRequiredMixin, generic.ListView):
    model = Breakdown
    queryset = Breakdown.objects.prefetch_related(
        "repair_staff", "equipment__type", "breakdown_type"
    )
    paginate_by = 8
    template_name = "log/log_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BreakdownListView, self).get_context_data(**kwargs)

        breakdown = self.request.GET.get("searched_breakdown", "")
        complete_status = self.request.GET.get("searched_complete_status")

        context["search_form"] = BreakdownSearchForm(
            initial={
                "searched_breakdown": breakdown,
                "searched_complete_status": complete_status,
            }
        )

        return context

    def get_queryset(self):
        form = BreakdownSearchForm(self.request.GET)
        queryset = self.queryset

        if form.is_valid():
            is_completed = form.cleaned_data["searched_complete_status"]
            queryset = queryset.filter(
                Q(
                    breakdown_type__name__icontains=form.cleaned_data[
                        "searched_breakdown"
                    ]
                )
                | Q(
                    equipment__type__name__icontains=form.cleaned_data[
                        "searched_breakdown"
                    ]
                )
                | Q(
                    equipment__name__icontains=form.cleaned_data[
                        "searched_breakdown"
                    ]
                )
            )
            if is_completed:
                queryset = queryset.filter(status="process")

        return queryset.distinct()


class BreakdownDetailView(LoginRequiredMixin, generic.DetailView):
    model = Breakdown
    fields = (
        "equipment",
        "breakdown_type",
        "repair_staff",
        "circumstance",
        "status",
        "repair_duration",
    )
    template_name = "log/log_detail.html"


class BreakdownCreateView(LoginRequiredMixin, generic.CreateView):
    model = Breakdown
    form_class = BreakdownForm
    template_name = "log/log_form.html"
    success_url = reverse_lazy("log:log-list")


class BreakdownUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Breakdown
    form_class = BreakdownForm
    template_name = "log/log_form.html"
    success_url = reverse_lazy("log:log-list")


class BreakdownDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Breakdown
    template_name = "log/log_detail.html"
    success_url = reverse_lazy("log:log-list")


class EquipmentTypeListView(LoginRequiredMixin, generic.ListView):
    model = EquipmentType
    queryset = EquipmentType.objects.all()
    paginate_by = 8
    template_name = "log/equipment_type_list.html"
    context_object_name = "equipment_type_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EquipmentTypeListView, self).get_context_data(**kwargs)

        equipment_type = self.request.GET.get("searched_equipment_type", "")
        context["search_form"] = EquipmentTypeSearchForm(
            initial={"searched_equipment_type": equipment_type}
        )

        return context

    def get_queryset(self):
        form = EquipmentTypeSearchForm(self.request.GET)
        if form.is_valid():
            return EquipmentType.objects.filter(
                name__icontains=form.cleaned_data["searched_equipment_type"]
            )


class EquipmentTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = EquipmentType
    form_class = EquipmentTypeForm
    template_name = "log/equipment_type_form.html"
    success_url = reverse_lazy("log:equipment-type-list")


class EquipmentTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EquipmentType
    form_class = EquipmentTypeForm
    context_object_name = "equipment_type"
    template_name = "log/equipment_type_form.html"
    success_url = reverse_lazy("log:equipment-type-list")


class EquipmentTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = EquipmentType
    context_object_name = "equipment_type"
    template_name = "log/equipment_type_form.html"
    success_url = reverse_lazy("log:equipment-type-list")


class EquipmentListView(LoginRequiredMixin, generic.ListView):
    model = Equipment
    queryset = Equipment.objects.select_related("type")
    paginate_by = 8
    template_name = "log/equipment_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EquipmentListView, self).get_context_data(**kwargs)

        equipment = self.request.GET.get("searched_equipment")
        context["search_form"] = EquipmentSearchForm(
            initial={"searched_equipment": equipment}
        )

        return context

    def get_queryset(self):
        form = EquipmentSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                Q(name__icontains=form.cleaned_data["searched_equipment"])
                | Q(
                    inventory_number__icontains=form.cleaned_data[
                        "searched_equipment"
                    ]
                )
                | Q(
                    type__name__icontains=form.cleaned_data[
                        "searched_equipment"
                    ]
                )
            ).distinct()


class EquipmentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = "log/equipment_form.html"
    success_url = reverse_lazy("log:equipment-list")


class EquipmentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = "log/equipment_form.html"
    success_url = reverse_lazy("log:equipment-list")


class EquipmentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Equipment
    template_name = "log/equipment_form.html"
    success_url = reverse_lazy("log:equipment-list")


class BreakdownTypeListView(LoginRequiredMixin, generic.ListView):
    model = BreakdownType
    queryset = BreakdownType.objects.all()
    paginate_by = 8
    context_object_name = "breakdown_type_list"
    template_name = "log/breakdown_type_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BreakdownTypeListView, self).get_context_data(**kwargs)

        breakdown_type = self.request.GET.get("searched_breakdown_type", "")
        context["search_form"] = BreakdownTypeSearchForm(
            initial={"searched_breakdown_type": breakdown_type}
        )

        return context

    def get_queryset(self):
        form = BreakdownTypeSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["searched_breakdown_type"]
            )


class BreakdownTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = BreakdownType
    form_class = BreakdownTypeForm
    template_name = "log/breakdown_type_form.html"
    success_url = reverse_lazy("log:breakdown-type-list")


class BreakdownTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = BreakdownType
    form_class = BreakdownTypeForm
    context_object_name = "breakdown_type"
    template_name = "log/breakdown_type_form.html"
    success_url = reverse_lazy("log:breakdown-type-list")


class BreakdownTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = BreakdownType
    template_name = "log/breakdown_type_form.html"
    context_object_name = "breakdown_type"
    success_url = reverse_lazy("log:breakdown-type-list")


@login_required
def toggle_perform_repair(request, pk):
    breakdown = Breakdown.objects.get(id=pk)

    if breakdown.status == "process":
        breakdown.status = "completed"
        breakdown.save()

    return HttpResponseRedirect(reverse_lazy("log:log-list"))
