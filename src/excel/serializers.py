from rest_framework import serializers


class CellPOSTSerializer(serializers.Serializer):
    value = serializers.CharField()


class CellGETSerializer(serializers.Serializer):
    value = serializers.CharField()
    result = serializers.CharField(default='ERROR')
