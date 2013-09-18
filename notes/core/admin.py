from django.contrib import admin

from .models import Note


class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'revision')


class NoteAdmin(DocumentAdmin):
    model = Note

admin.site.register(Note, NoteAdmin)
