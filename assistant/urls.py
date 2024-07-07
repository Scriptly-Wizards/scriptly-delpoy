# urls.py
from django.urls import path
from .views import VideoDataView
# from .views import MusicDataView
from .views import GeneratePDFView

urlpatterns = [
    path('v1/assistant/', VideoDataView.as_view(), name='assistant'),
    # path('v1/assistant/music/', MusicDataView.as_view(), name='assistant-music'),
    path('v1/assistant/pdf/', GeneratePDFView.as_view(), name='assistant-pdf'),
]
