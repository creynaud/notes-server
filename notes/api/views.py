from django.utils.decorators import method_decorator
from django.views.decorators.http import etag

from rest_framework.response import Response
from rest_framework import viewsets, permissions, mixins
from rest_framework.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from ..core.models import Note
from .serializers import NoteSerializer, NoteUUIDAndRevisionSerializer


def etag_note(request, uuid):
    if uuid:
        try:
            return Note.objects.get(uuid=uuid).revision
        except Note.DoesNotExist:
            pass
    else:
        return None


class DocumentViewSetMixin(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(etag(etag_func=etag_note))
    def retrieve(self, request, *args, **kwargs):
        return super(DocumentViewSetMixin, self).retrieve(request, *args,
                                                          **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        revision = request.QUERY_PARAMS.get('revision')
        if not revision:
            data = {
                "error": "You must specify a 'revision' query parameter"
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if obj.revision != revision:
            data = {
                "error": ("Conflict, you are trying to delete an old revision "
                          "of this object")
            }
            return Response(data, status=HTTP_409_CONFLICT)
        return super(DocumentViewSetMixin, self).destroy(request, *args,
                                                         **kwargs)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        revision = request.DATA.get('revision')
        if not revision:
            data = {
                "error": "You must specify a 'revision' in the request data"
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if obj.revision != revision:
            data = {
                "error": ("Conflict, you are trying to update an old revision "
                          "of this object")
            }
            return Response(data, status=HTTP_409_CONFLICT)
        return super(DocumentViewSetMixin, self).update(request, *args,
                                                        **kwargs)


class NotesViewSet(DocumentViewSetMixin):
    model = Note
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteUUIDAndRevisionViewSet(mixins.ListModelMixin, GenericViewSet):
    model = Note
    serializer_class = NoteUUIDAndRevisionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
