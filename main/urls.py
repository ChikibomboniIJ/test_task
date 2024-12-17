from django.urls import path, include
from .routers import router_tasks

urlpatterns = [
    path('', include(router_tasks.urls)),
]
