from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'notes', views.NotesViewSet)

# We include the login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
