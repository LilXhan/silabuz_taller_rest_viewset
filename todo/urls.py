from rest_framework.routers import DefaultRouter

from .views import TodoViewSetCustom, TodoViewSet

router = DefaultRouter()

router.register('v1/todo', TodoViewSetCustom, basename='todosCustom')
router.register('v2/todo', TodoViewSet, basename='todos')

urlpatterns = router.urls
