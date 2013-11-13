from django.contrib.auth.models import User

from factory import lazy_attribute, Sequence
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory

from notes.core.models import Note


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User
    username = Sequence(lambda n: 'the_brain{0}@acme.com'.format(n))

    @lazy_attribute
    def email(self):
        return self.username


class NoteFactory(DjangoModelFactory):
    FACTORY_FOR = Note
    owner = SubFactory(UserFactory)

    @lazy_attribute
    def text(self):
        return "Some text"

    @lazy_attribute
    def title(self):
        return "Title"
