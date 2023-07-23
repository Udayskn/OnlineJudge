from .models import Problem
from django.shortcuts import render, redirect, get_object_or_404
from home.forms import CodeForm
from django.views import generic
class ProblemListView(generic.ListView):
    template_name = 'home\Problemset.html'
    context_object_name = 'Problem_list'

    def get_queryset(self):
        return Problem.objects.all()
def ProblemDetail(request, problem_id):
    # if request.method=='POST':
    #     language=request.POST['language']
    #     code=request.POST['code']
    #     return redirect('verdict/')
    problem = get_object_or_404(Problem, id=problem_id)
    form = CodeForm()
    context = {
        'ProblemName': problem.problem_name,
        'Problemstatement': problem.problem_statement,
        'problem_id': problem.id,
        'problem': problem,
    }
    return render(request, 'home\problempage.html', context)

def Verdict(request, problem_id):
    # extract data from form
    form = CodeForm(request.POST)
    user_code = ''
    if form.is_valid():
        user_code = form.cleaned_data.get('user_code')
        user_code = user_code.replace('\r\n','\n').strip()
        
    language = request.POST['language']
    return render(request, 'home\problempage.html')