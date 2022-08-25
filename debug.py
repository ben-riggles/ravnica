from ravnica import models, serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io


rec = models.Record(wins=10, losses=7)
ser = serializers.RecordSerializer(rec)
print(ser.data)

json = JSONRenderer().render(ser.data)
print(json)

data = JSONParser().parse(io.BytesIO(json))
print(data)

ser = serializers.RecordSerializer(data=data)
if ser.is_valid():
    print(ser.validated_data)