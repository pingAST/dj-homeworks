from rest_framework import generics
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer


class SensorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all().order_by('-id')
    serializer_class = SensorSerializer


class SensorDetailRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementCreateAPIView(generics.CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
