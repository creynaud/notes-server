from rest_framework import serializers

from ..core.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['uuid', 'revision', 'date', 'title', 'text']

    def restore_object(self, attrs, instance=None):
        note = super(NoteSerializer, self).restore_object(attrs, instance)
        note.owner = self.context['request'].user
        return note


class NoteUUIDAndRevisionSerializer(NoteSerializer):
    class Meta:
        model = Note
        fields = ['uuid', 'revision']
