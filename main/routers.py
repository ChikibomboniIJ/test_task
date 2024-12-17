from rest_framework.routers import DefaultRouter
from .views import TaskModelViewSet

router_tasks = DefaultRouter()
router_tasks.register(r'task', TaskModelViewSet)