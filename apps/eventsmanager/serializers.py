from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Event, Extractor

#serializer for an event
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'keywords', 'startEventDate', 'endEventDate', 'detailsURL', 'detailsURL', 'geoLocation', 'relatedVisualisation', 'languageID', 'userID', 'externalResourceID', 'dateAddedToPC', 'dateIssuedByExternalResource', 'dateModified', 'viewsCount')

from apps.eventsmanager.models import (
    Event,
)
#serializer for the extractor model
class ExtractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extractor

class ExternalEventSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    url = serializers.CharField()
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()