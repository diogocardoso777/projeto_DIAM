from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import validate_email
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .models import Post, Forum, Client, Seller


def index(request):
    post_list = Post.objects.order_by('-created_at')
    context = {
        'post_list': post_list,
    }
    return render(request, 'sports24h/index.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def post(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/create_post.html')
    title = request.POST.get('title', '')
    forum = request.POST.get('forum', '')
    description = request.POST.get('description', '')
    if title and forum and description:
        p = Post(owner=request.user, forum=forum, title=title, text=description)
        p.save()
    return HttpResponseRedirect(reverse('sports24h:index'))


def forums_index(request):
    forum_list = Forum.objects.order_by('-name')
    context = {
        'forum_list': forum_list,
    }
    return render(request, 'sports24h/forums_index.html', context)


def forum(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/create_forum.html')
    name = request.POST.get('forum_name', '')
    genre = request.POST.get('genre', '')
    if name and genre:
        forum = Forum(name=name, genre=genre)
        forum.save()
        forum.save()
    return HttpResponseRedirect(reverse('sports24h:forums_index'))


def register_user(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/register.html')

    username = request.POST.get('username')
    user_type = request.POST.get('user_type')
    email = request.POST.get('email')
    passwd = request.POST.get('password')
    birthdate_str = request.POST.get('birthdate')

    # Check if any of the required fields are empty
    if not (username and user_type and email and passwd and birthdate_str):
        context = {
            'error_message': "Por favor, preencha todos os campos obrigatórios.",
        }
        return render(request, 'sports24h/register.html', context=context)

    if User.objects.filter(username=username).exists():
        context = {
            'error_message': "O nome de utilizador não se encontra disponível! Por favor, escolha outro.",
        }
        return render(request, 'sports24h/register.html', context)

    try:
        validate_email(email)
    except ValidationError:
        # Invalid email format
        # Add an error message to the context and render the form again
        context = {
            'error_message': "Por favor, introduza um endereço de email válido.",
        }
        return render(request, 'sports24h/register.html', context=context)

    if len(passwd) < 1:  # TODO mudar na versao final para 8
        # Password is too short
        # Add an error message to the context and render the form again
        context = {
            'error_message': "A password deve ter pelo menos 8 caracteres.",
        }
        return render(request, 'sports24h/register.html', context=context)

    birthdate = date.fromisoformat(birthdate_str)
    if (date.today() - birthdate).days < 365 * 18:
        # User is not yet 18 years old
        # Add an error message to the context and render the form again
        context = {
            'error_message': "Tem de ter pelo menos 18 anos para se registar.",
        }
        return render(request, 'sports24h/register.html', context=context)

    u = User.objects.create_user(username=username, email=email, password=passwd)

    if user_type == 'client':
        c = Client(user=u, birthdate=birthdate)
        c.save()
    elif user_type == 'seller':
        s = Seller(user=u, birthdate=birthdate)
        s.save()
    return HttpResponseRedirect(reverse('sports24h:login_user'))


def login_user(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/login.html')
    username = request.POST['username']
    passwd = request.POST['password']

    if username and passwd:
        user = authenticate(username=username, password=passwd)

    if user is not None:
        # user exists
        login(request, user)
        # a = Aluno.objects.get(user=user)
        # request.session['curso'] = a.curso
        # request.session['num_votos'] = a.votos
        # request.session['foto'] = a.foto
        return HttpResponseRedirect(reverse('sports24h:index'))
    else:
        # user doesn't exist
        context = {
            'error_message': "O utilizador não existe na base de dados! Por favor, verifique se os dados introduzidos "
                             "estão corretos.",
        }
        return render(request, 'sports24h/login.html', context)


def logout_user(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/logout.html')
    logout(request)
    # direccionar para página de sucesso
    return HttpResponseRedirect(reverse('sports24h:index'))


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def profile(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/profile.html')


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def upload_photo(request):
    if request.method == 'POST' and len(request.FILES) == 0:
        return render(request, 'sports24h/profile.html',
                      {'uploaded_file_status': "Please select a photo"})
    if request.method == 'POST' and request.FILES['myfile']:
        fs = FileSystemStorage()
        myfile = request.FILES['myfile']
        filename = fs.save(myfile.name, myfile)
        c = Client.objects.get(user=request.user)
        c.foto = "media/" + filename
        c.save()
        request.session['foto'] = c.foto
        return render(request, 'sports24h/profile.html',
                      {'uploaded_file_status': "Photo updated successfully"})


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def reset_foto(request):
    c = Client.objects.get(user=request.user)
    c.foto = "media/default_icon.png"
    request.session['foto'] = c.foto
    c.save()
    return render(request, 'profile/profile.html',
                  {'uploaded_file_status': "Photo removed successfully"})


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def shopping_cart(request):
    if request.method != "POST":
        return render(request, 'sports24h/shoppping_cart.html')

#
# #### utility functions ####
#
# def is_valid_field(type, value):
#     if type == "email":
#         try:
#             validate_email(value)
#         except ValidationError:
#             return False
#     elif type == "passwd":
#         if len(value) < 8:
#             return False
#     elif type == "birthdate":
#         try:
#             birthdate = date.fromisoformat(value)
#             if (date.today() - birthdate).days < 365 * 18:
#                 return False
#         except ValueError:
#             return False
#
#     return True
