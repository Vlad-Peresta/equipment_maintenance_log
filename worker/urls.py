from django.contrib.auth.views import LogoutView
from django.urls import path

from worker.views import (
    login_view,
    register_worker,
    WorkerListView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerCreateView,
    WorkerDeleteView,
)

app_name = "worker"

urlpatterns = [
    path("accounts/login/", login_view, name="worker-login"),
    path("accounts/logout/", LogoutView.as_view(), name="worker-logout"),
    path("accounts/register/", register_worker, name="worker-register"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
]
