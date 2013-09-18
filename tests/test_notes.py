from django.core.urlresolvers import reverse

from django_webtest import WebTest
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND
from tests.factories import NoteFactory


class NotesTest(WebTest):
    def test_my_notes(self):
        url = reverse('my_notes')
        self.app.get(url, status=HTTP_302_FOUND)

        note = NoteFactory.create(title='Title', text='Some text.')
        response = self.app.get(url, user=note.owner.username,
                                status=HTTP_200_OK)
        self.assertContains(response, note.title)
        self.assertContains(response, note.text)
