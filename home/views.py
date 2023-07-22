from .models import Problem
from django.views import generic
class ProblemListView(generic.ListView):
    template_name = 'home\Problemset.html'
    context_object_name = 'Problem_list'

    def get_queryset(self):
        return Problem.objects.all()
class ProblemDetailView(generic.DetailView):
    model =Problem
    template_name='home\problempage.html'