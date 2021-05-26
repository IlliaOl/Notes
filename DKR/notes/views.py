from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from .models import Note
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import NoteForm
from django.urls import reverse_lazy


class List(LoginRequiredMixin, ListView):
	model = Note
	template_name = 'note.html'
	login_url = 'login'
	paginate_by = 5
	ordering = ['-created']


class Create(LoginRequiredMixin, CreateView):
	model = Note
	template_name = 'note_new.html'
	form_class = NoteForm
	success_url = reverse_lazy('note_list')
	login_url = 'login'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class HomePage(TemplateView):
	template_name = 'index.html'


class Update(LoginRequiredMixin, UpdateView):
	model = Note
	form_class = NoteForm
	template_name = 'note_edit.html'
	success_url = reverse_lazy('note_list')
	login_url = 'login'


class Delete(LoginRequiredMixin, DeleteView):
	model = Note
	template_name = 'note_delete.html'
	success_url = reverse_lazy('note_list')
	login_url = 'login'






