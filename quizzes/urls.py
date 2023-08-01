from django.urls import include, path

from .views import router, CreateUserView, CompleteTest

urlpatterns = [
    path('', include(router.urls)),
    path('register/', CreateUserView.as_view()),
    path('test/', CompleteTest.as_view()),
]
