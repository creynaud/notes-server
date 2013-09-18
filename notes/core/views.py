from django.contrib.auth.decorators import login_required
from django.views import generic

from .models import Note


class MyNotes(generic.ListView):
    model = Note
    template_name = "core/my_notes.html"

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
my_notes = login_required(MyNotes.as_view())
