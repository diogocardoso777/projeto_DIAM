from django.contrib.auth import authenticate, login
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'sports24h/index.html')


def login_utilizador(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/login.html')
    username = request.POST['username']
    passwd = request.POST['password']
    user = authenticate(username=username, password=passwd)

    if user is not None:
        # user exists
        login(request, user)
        # ir buscar o aluno de forma a conseguir o curso
        #a = Aluno.objects.get(user=user)
        #request.session['curso'] = a.curso
        #request.session['num_votos'] = a.votos
        #request.session['foto'] = a.foto
        #return HttpResponseRedirect(reverse('votacao:index'))
    else:
        # user doesn't exist
        context = {
            'error_message': "O utilizador não existe na base de dados! Por favor, verifique se os dados introduzidos "
                             "estão corretos.",
        }
        #return render(request, 'votacao/erro.html', context)
