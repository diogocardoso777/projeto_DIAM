from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.validators import validate_email
from django.db.models import Subquery
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Message, Product, Size, ShoppingCart, Follows
from .models import Message, FollowsForum
from .models import Post, Forum, Client, Seller, Country, Team, Sport
from django.db import IntegrityError

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy

from .models import Post, Forum, Client, Seller, Country, Team, Sport


def index(request):  # TODO mostrar apenas artigos ativos
    post_list = Post.objects.order_by('-created_at')
    if request.user.is_authenticated:
        try:
            u = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            u = Seller.objects.get(user=request.user)
        product_list = Product.objects.order_by('-created_at')
        context = {
            'post_list': post_list,
            'product_list': product_list,
            'user': u
        }
        return render(request, 'sports24h/index.html', context)
    else:
        return render(request, 'sports24h/login.html')


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def post(request):
    if not request.method == 'POST':
        forum_list = Forum.objects.order_by('-name')
        context = {
            'forum_list': forum_list,
        }
        return render(request, 'sports24h/create_post.html', context)
    title = request.POST.get('title', '')
    forum = request.POST.get('forum', '')
    text = request.POST.get('text', '')
    s = Seller.objects.get(user=request.user)
    if title and forum and text:
        f = Forum.objects.get(name=forum)
        p = Post(owner=s, forum=f, title=title, text=text)
        p.save()
    return HttpResponseRedirect(reverse('sports24h:index'))


@login_required(login_url=reverse_lazy('sports24h:login_user'))  # TODO permitir seller ter acesso a esta view
def product(request):
    if not request.method == 'POST':
        forum_list = Forum.objects.order_by('-name')
        size_list = Size.objects.order_by('-name')
        context = {
            'forum_list': forum_list,
            'size_list': size_list
        }
        return render(request, 'sports24h/create_product.html', context)
    name = request.POST.get('name')
    size = request.POST.get('size')
    forum = request.POST.get('forum')
    price = request.POST.get('price')
    photo = request.FILES['photo']
    if name and size and photo and forum and price:
        seller = Seller.objects.get(user=request.user)
        s = Size.objects.get(name=size)
        f = Forum.objects.get(name=forum)
        p = Product(owner=seller, name=name, size=s, photo=photo, price=price, forum=f)
        p.save()
        return HttpResponseRedirect(reverse('sports24h:index'))
    else:
        context = {
            'error_message': "Please, check if the fields are correctly filled.",
        }
        return render(request, 'sports24h/product.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def follow_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        follows, created = Follows.objects.get_or_create(following_user=request.user, followed_user=user)
        if created:
            follows.save()
            return redirect('sports24h:search_users')
        else:
            return redirect('sports24h:search_users')


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def search_users(request):
    if not request.method == 'POST':
        followed_user_ids = Follows.objects.filter(
            following_user=request.user
        ).values_list('followed_user__id', flat=True)
        followed_users = User.objects.filter(
            id__in=followed_user_ids
        )
        context = {
            'followed_users': followed_users
        }

        return render(request, 'sports24h/search_users.html', context)
    search_query = request.POST.get('search_query')
    followed_user_ids = Follows.objects.filter(
        following_user=request.user
    ).values_list('followed_user__id', flat=True)

    # filter the search results to exclude followed users
    users = User.objects.filter(
        username__icontains=search_query
    ).exclude(
        id=request.user.id
    ).exclude(
        id__in=followed_user_ids
    )

    # get the list of User objects of the followed users
    followed_users = User.objects.filter(
        id__in=followed_user_ids
    )

    context = {
        'users': users,
        'followed_users': followed_users
    }
    return render(request, 'sports24h/search_users.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def unfollow_user(request):
    user_id = request.POST.get('user_id')
    followed_user = get_object_or_404(User, id=user_id)
    if user_id is not None:
        follow = Follows.objects.get(following_user=request.user, followed_user=followed_user)
        follow.delete()
    return redirect('sports24h:search_users')


# handle invalid user_id value


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'sports24h/product_detail.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def post_detail(request, post_id):
    post = get_object_or_404(Product, pk=post_id)
    context = {
        'post': post
    }
    return render(request, 'sports24h/post_detail.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def size(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/create_size.html')
    name = request.POST.get('name')
    if name:
        s = Size(name=name)
        s.save()
        return HttpResponseRedirect(reverse('sports24h:index'))
    else:
        context = {
            'error_message': "Please, check if the fields are correctly filled.",
        }
        return render(request, 'sports24h/create_size.html', context=context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def sport(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/create_sport.html')
    name = request.POST.get('name')
    if name:
        s = Sport(name=name)
        s.save()
        return HttpResponseRedirect(reverse('sports24h:index'))
    else:
        context = {
            'error_message': "Please, check if the fields are correctly filled.",
        }
        return render(request, 'sports24h/create_sport.html', context=context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def country(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/create_country.html')
    name = request.POST.get('name')
    if name:
        c = Country(name=name)
        c.save()
        return HttpResponseRedirect(reverse('sports24h:index'))
    else:
        context = {
            'error_message': "Please, check if the fields are correctly filled.",
        }
        return render(request, 'sports24h/create_country.html', context=context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def team(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/create_team.html')
    name = request.POST.get('name')
    if name:
        t = Team(name=name)
        t.save()
        return HttpResponseRedirect(reverse('sports24h:index'))
    else:
        context = {
            'error_message': "Please, check if the fields are correctly filled.",
        }
        return render(request, 'sports24h/team.html', context=context)


def forums_index(request):
    user_followed_forums = request.user.followsforum_set.all().values_list('forum__id', flat=True)
    forum_list = Forum.objects.exclude(id__in=user_followed_forums).order_by('-name')
    followed_forums = Forum.objects.filter(id__in=user_followed_forums).order_by('-name')
    context = {
        'forums': forum_list,
        'followed_forums': followed_forums,
    }
    return render(request, 'sports24h/forums_index.html', context)


def follow_forum(request):
    if not request.method == 'POST':
        return forums_index(request)

    forum_id = request.POST.get('forum_id')
    forum = get_object_or_404(Forum, pk=forum_id)
    try:
        follow = FollowsForum.objects.create(user=request.user, forum=forum)
    except IntegrityError:
        context = {
            'message': "You are already following the forum " + forum.name,
        }
    else:
        context = {
            'message': "You followed the forum " + forum.name,
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
    return HttpResponseRedirect(reverse('sports24h:forums_index'))


def register_user(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/register.html')
    passwd = request.POST.get('password')
    confirm_passwd = request.POST.get('confirm_password')

    if passwd != confirm_passwd:
        context = {
            'error_message': "Passwords não coincidem",
        }
        return render(request, 'sports24h/register.html', context=context)
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
def set_country(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        c = Client.objects.get(user=request.user)
        if country:
            country, created = Country.objects.get_or_create(name=country)
            c.country = country
            c.save()
            request.user = c
            return render(request, 'sports24h/profile.html',
                          {'set_profile_setting': "Profile changed successfully"})
    return render(request, 'sports24h/profile.html',
                  {'set_profile_setting': "Error trying to change the profile"})


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def set_favoriteTeam(request):
    if request.method == 'POST':
        teamCountry = request.POST.get('teamCountry')
        teamName = request.POST.get('teamName')
        c = Client.objects.get(user=request.user)
        if teamCountry and teamName:
            country, created = Country.objects.get_or_create(name=teamCountry)
            if created:
                country.save()
            team, created = Team.objects.get_or_create(name=teamName, country=country)
            if created:
                team.save()
            c.favorite_team = team
            c.save()
            request.user = c
            return render(request, 'sports24h/profile.html',
                          {'set_profile_setting': "Profile changed successfully"})

    return render(request, 'sports24h/profile.html',
                  {'set_profile_setting': "Error trying to change the profile"})


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def set_favoriteSport(request):
    if request.method == 'POST':
        sportName = request.POST.get('sportName')
        c = Client.objects.get(user=request.user)
        if sportName:
            sport, created = Sport.objects.get_or_create(name=sportName)
            if created:
                sport.save()
            c.favorite_sport = sport
            c.save()
            request.user = c
            return render(request, 'sports24h/profile.html',
                          {'set_profile_setting': "Profile changed successfully"})

    return render(request, 'sports24h/profile.html',
                  {'set_profile_setting': "Error trying to change the profile"})


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
        try:
            client = Client.objects.get(user=request.user)
            cart = ShoppingCart.objects.get(client=client)
            cart_items = cart.product_list.all()
        except ObjectDoesNotExist:
            cart_items = []

        context = {
            'cart_items': cart_items,
        }
        return render(request, 'sports24h/shopping_cart.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def add_to_cart(request, product_id):
    if not hasattr(request.user, 'client'):
        # Redirect or handle the case where the user is not a Client
        return HttpResponseRedirect(reverse('sports24h:index'))

    client = Client.objects.get(user=request.user)

    try:
        shopping_cart = ShoppingCart.objects.get(client=client)
    except ObjectDoesNotExist:
        # Create a new ShoppingCart object for the client
        shopping_cart = ShoppingCart.objects.create(client=client)

    product = Product.objects.get(id=product_id)
    shopping_cart.product_list.add(product)

    # Optionally, you can redirect the user to a success page or display a message
    return HttpResponseRedirect(reverse('sports24h:index'))


def send_message_html(request):
    return render(request, 'sports24h/send_message.html')


def about_index(request):
    return render(request, 'sports24h/about.html')


def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    return render(request, 'sports24h/send_message.html', {'messages': messages})


def send_message_submit(request):
    if request.method == 'POST':
        recipient_username = request.POST['recipient']
        content = request.POST['message']

        try:
            recipient = User.objects.get(username=recipient_username)
            message = Message(sender=request.user, recipient=recipient, content=content)
            message.save()
            return redirect('sports24h:index')  # Redirect to the main page after sending the message
        except User.DoesNotExist:
            return render(request, 'sports24h/send_message.html', {'error': 'Destinatário não encontrado'})

    return render(request, 'sports24h/send_message.html')
