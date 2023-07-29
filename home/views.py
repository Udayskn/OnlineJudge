from .models import Problem,TestCase
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from home.forms import CodeForm
from django.views import generic
from time import time
import os
import signal
import subprocess
import os.path
import docker

class ProblemListView(generic.ListView):
    template_name = 'home\Problemset.html'
    context_object_name = 'Problem_list'

    def get_queryset(self):
        return Problem.objects.all()
def ProblemDetail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    form = CodeForm()
    context = {
        'ProblemName': problem.problem_name,
        'Problemstatement': problem.problem_statement,
        'problem_id': id,
        'problem': problem,
    }
    return render(request, 'home\problempage.html', context)

def Verdict(request, problem_id):
    # extract data from form
    form = CodeForm(request.POST)
    user_code = 'Not_valid'
    if form.is_valid():
        user_code = form.cleaned_data.get('user_code')
        user_code = user_code.replace('\r\n','\n').strip()
    user_code=request.POST['code']    
    language = request.POST['language']
    
    if request.method == 'POST':
        # setting docker-client
        docker_client = docker.from_env()
        Running = "running"
        problem = Problem.objects.get(id=problem_id)
        testcase = TestCase.objects.get(problem_id=problem_id)
        #replacing \r\n by \n in original output to compare it with the usercode output
        testcase.output = testcase.output.replace('\r\n','\n').strip() 
        filename=str(problem.id)
        
        if language == "C++":
                extension = ".cpp"
                cont_name = "oj-cpp"
                compile = f"g++  {filename}.cpp"
                clean = f" {filename}.cpp"
                docker_img = "gcc:11.2.0"
                exe = f"./{filename}.out"
        file = filename + extension
        filepath = settings.FILES_DIR + "/" + file
        code = open(filepath,"w")
        code.write(user_code)
        code.close()
        print(filepath)
        # checking if the docker container is running or not
        try:
            container = docker_client.containers.get(cont_name)
            container_state = container.attrs['State']
            container_is_running = (container_state['Status'] == Running)
            if not container_is_running:
                subprocess.run(f"docker start {cont_name}",shell=True)
        except docker.errors.NotFound:
            subprocess.run(f"docker run -dt --name {cont_name} {docker_img}",shell=True)
        res="Not compiled"
        verdict="Wrong Answer"
         # copy/paste the .cpp file in docker container 
        
        t=subprocess.run(f"docker cp {filepath} {cont_name}:/{file}",shell=True)
        if(file):
            print("q",file)
            print("p",filepath)
            subprocess.run(f"docker cp {filepath} {cont_name}:/{file}",shell=True)
        # compiling the code
        cmp = subprocess.run(f"docker exec {cont_name} {compile}", capture_output=True, shell=True)
        if(cmp):
            print("cmp")
            print(cmp)
        if cmp.returncode != 0:
            verdict = "Compilation Error"
            # subprocess.run(f"docker exec {cont_name} rm {file}",shell=True)

        else:
            # running the code on given input and taking the output in a variable in bytes
            start = time()
            try:
                res = subprocess.run( f'docker exec -it {cont_name} sh -c "echo \'{testcase.input}\' | ./a.out"' ,
                                                capture_output=True, timeout=1000000,shell=True)
                # res = subprocess.run(f" docker exec -it  {cont_name} sh -c "echo "5 4 3 2 1" | {exe}.out" ",
                #                                 capture_output=True, timeout=100000, shell=True)
                if(res):
                    print("res")
                    print(res)
                run_time = time()-start
                subprocess.run(f"docker exec {cont_name} rm {clean}",shell=True)
            except subprocess.TimeoutExpired:
                run_time = time()-start
                verdict = "Time Limit Exceeded"
                subprocess.run(f"docker container kill {cont_name}", shell=True)
                subprocess.run(f"docker start {cont_name}",shell=True)
                subprocess.run(f"docker exec {cont_name} rm {clean}",shell=True)
            if verdict != "Time Limit Exceeded" and res.returncode != 0:
                verdict = "Runtime Error"
                

        user_stderr = ""
        user_stdout = ""
        if verdict == "Compilation Error":
            user_stderr = cmp.stderr.decode('utf-8')
        
        elif verdict == "Wrong Answer":
            print("l",testcase.output)
            user_stdout = res.stdout.decode('utf-8')
            print("p",user_stdout)
            if str(user_stdout)==str(testcase.output):
                verdict = "Accepted"
            testcase.output += '\n' # added extra line to compare user output having extra line at the end of their output
            if str(user_stdout)==str(testcase.output):
                verdict = "Accepted"


        context={
        'Code': user_code,
        'lang': language,
        'res':res,
        'verdict':verdict,
        'user_stderr':user_stderr,
        'user_stdout': user_stdout
        }
                
    return render(request, 'home\problemverdict.html', context)