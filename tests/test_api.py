from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories import NoteFactory, UserFactory

from notes.core.models import Note


class APITestNotAuthenticated(APITestCase):
    def test_get_notes_not_authenticated(self):
        url = reverse('note-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_notes_uuids_not_authenticated(self):
        url = reverse('notes-uuids-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_note_not_authenticated(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_note_not_authenticated(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_note_not_authenticated(self):
        url = reverse('note-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_note_not_authenticated(self):
        url = reverse('note-list')
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class APITestAuthenticated(APITestCase):
    def test_get_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-detail', args=['dummy'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-detail', args=['dummy'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-list', args=['dummy'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-list', args=['dummy'])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_notes(self):
        user1 = UserFactory.create()
        note1 = NoteFactory.create(owner=user1)

        user2 = UserFactory.create()
        note2 = NoteFactory.create(owner=user2)

        url = reverse('note-list')
        self.client.force_authenticate(user=user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, note1.uuid)
        self.assertContains(response, note1.revision)
        self.assertContains(response, note1.text)
        self.assertContains(response, note1.title)
        self.assertNotContains(response, note2.uuid)

    def test_get_notes_uuids(self):
        user1 = UserFactory.create()
        note1 = NoteFactory.create(owner=user1)

        user2 = UserFactory.create()
        note2 = NoteFactory.create(owner=user2)

        url = reverse('notes-uuids-list')
        self.client.force_authenticate(user=user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, note1.uuid)
        self.assertContains(response, note1.revision)
        self.assertNotContains(response, note1.text)
        self.assertNotContains(response, note1.title)
        self.assertNotContains(response, note2.uuid)
        self.assertNotContains(response, note2.revision)

    def test_get_note(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        self.client.force_authenticate(user=note.owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({'uuid': note.uuid}, response.data)
        self.assertDictContainsSubset({'revision': note.revision},
                                      response.data)
        self.assertDictContainsSubset({'text': note.text}, response.data)
        self.assertDictContainsSubset({'date': note.date}, response.data)

    def test_delete_note_no_revision(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.owner)
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_note_invalid_revision(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.owner)
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.delete(url + "?revision=dummy")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        expected_response_data = {
            "error": ("Conflict, you are trying to delete an old revision "
                      "of this object")
        }
        self.assertDictContainsSubset(expected_response_data, response.data)

    def test_delete_note(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.owner)
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.delete(url + "?revision={0}".format(
            note.revision))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_new_note(self):
        user = UserFactory.create()
        url = reverse('note-list')
        data = {
            "uuid": "06e35afa-36fb-46cd-bd80-dce6560e3b7b",
            "date": "2013-09-10T20:33:40Z",
            "text": "This is a test",
            "title": "Title",
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        note = Note.objects.get(uuid=data['uuid'])
        self.assertEqual(note.text, data['text'])
        self.assertEqual(note.title, data['title'])
        self.assertIsNotNone(note.date)
        self.assertEqual(note.owner.email, user.email)

    def test_put_note(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "date": "2013-09-10T20:33:40Z",
            "text": "This is a test",
            "title": "Title",
        }
        self.client.force_authenticate(user=note.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note = Note.objects.get(uuid=data['uuid'])
        self.assertEqual(note.text, data['text'])
        self.assertEqual(note.title, data['title'])
        self.assertIsNotNone(note.date)

    def test_put_note_no_revision(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "date": "2013-09-10T20:33:40Z",
            "text": "This is a test",
            "title": "Title",
        }
        self.client.force_authenticate(user=note.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note_invalid_revision(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": "invalid",
            "date": "2013-09-10T20:33:40Z",
            "text": "This is a test",
            "title": "Title",
        }
        self.client.force_authenticate(user=note.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        expected_response_data = {
            "error": ("Conflict, you are trying to update an old revision "
                      "of this object")
        }
        self.assertDictContainsSubset(expected_response_data, response.data)
