from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from .models import Note
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import NoteForm
from django.urls import reverse_lazy


class NoteListView(LoginRequiredMixin, ListView):
	model = Note
	template_name = 'note.html'
	login_url = 'login'
	paginate_by = 5
	ordering = ['-created']


class MyNoteListView(LoginRequiredMixin, ListView):
	model = Note
	template_name = 'my_notes.html'
	login_url = 'login'
	paginate_by = 5
	ordering = ['-created']
	def get_queryset(self):
		return Note.objects.filter(author=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
	model = Note
	template_name = 'note_new.html'
	form_class = NoteForm
	success_url = reverse_lazy('note_list')
	login_url = 'login'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class HomePageView(TemplateView):
	template_name = 'index.html'


class NoteUpdateView(LoginRequiredMixin, UpdateView):
	model = Note
	form_class = NoteForm
	template_name = 'note_edit.html'
	success_url = reverse_lazy('note_list')
	login_url = 'login'


class NoteDeleteView(LoginRequiredMixin, DeleteView):
	model = Note
	template_name = 'note_delete.html'
	success_url = reverse_lazy('note_list')
	login_url = 'login'






