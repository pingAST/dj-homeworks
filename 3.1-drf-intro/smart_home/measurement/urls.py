from django.urls import path
from .views import SensorListCreateAPIView, SensorDetailRetrieveUpdateAPIView, MeasurementCreateAPIView

urlpatterns = [
    path('sensors/', SensorListCreateAPIView.as_view(), name='sensor-list-create'),
    path('sensors/<int:pk>/', SensorDetailRetrieveUpdateAPIView.as_view(), name='sensor-detail-retrieve'),
    path('measurements/', MeasurementCreateAPIView.as_view(), name='measurement-create'),

]
