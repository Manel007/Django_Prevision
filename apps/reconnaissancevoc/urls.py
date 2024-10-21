from django.urls import path, re_path
from .views import SpeechToTextView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('transcribe/', SpeechToTextView.as_view(), name='transcribe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)