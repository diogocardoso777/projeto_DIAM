from datetime import date
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.db.models import Subquery
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Message, Product, Size, ShoppingCart, Follows, Comment, Likes, BoughtProducts, SellerProduct, Review,  FollowsForum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from .models import Post, Forum, Client, Seller, Country, Team, Sport
from .serializers import PostSerializer, CommentSerializer, UserSerializer, OwnerSerializer

from django.contrib.auth import get_user_model

@login_required(login_url=reverse_lazy('sports24h:login_user'))
def index(request):
    user_type = None
    is_seller = False  # Initialize is_seller as False

    if hasattr(request.user, 'client'):
        user_type = 'client'
    elif hasattr(request.user, 'seller'):
        user_type = 'seller'
        is_seller = True

    post_list = Post.objects.order_by('-created_at')
    liked_posts = Post.objects.filter(likes__user=request.user)
    product_list = Product.objects.order_by('-created_at')


    if user_type == 'client':
        User = get_user_model()
        client_user = User.objects.get(client=request.user.client)
        followed_forums = FollowsForum.objects.filter(user=client_user)

        followed_forums_post = []
        for forum in followed_forums:
            forum_posts = Post.objects.filter(forum=forum.forum)
            followed_forums_post += forum_posts
    else:
        User = get_user_model()
        client_user = User.objects.get(seller=request.user.seller)
        followed_forums = FollowsForum.objects.filter(user=client_user)

        followed_forums_post = []
        for forum in followed_forums:
            forum_posts = Post.objects.filter(forum=forum.forum)
            followed_forums_post += forum_posts
    request.session['user_type'] = user_type
    context = {
        'post_list': post_list,
        'product_list': product_list,
        'user': request.user,
        'is_seller': is_seller,
        'liked_posts': liked_posts,
        'followed_forums_post': followed_forums_post,
    }

    return render(request, 'sports24h/index.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def posts_index(request):         # TODO mostrar apenas artigos ativos
    post_list = Post.objects.order_by('-created_at')
    liked_posts = Post.objects.filter(likes__user=request.user)
    product_list = Product.objects.order_by('-created_at')
    is_seller = Seller.objects.filter(user=request.user).exists()
    context = {
        'post_list': post_list,
        'product_list': product_list,
        'user': request.user,
        'liked_posts': liked_posts,
        'is_seller': is_seller
    }
    return render(request, 'sports24h/posts_index.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def products_index(request):         # TODO mostrar apenas artigos ativos
    product_list = Product.objects.order_by('-created_at')
    is_seller = Seller.objects.filter(user=request.user).exists()
    context = {
        'product_list': product_list,
        'user': request.user,
        'is_seller': is_seller
    }
    return render(request, 'sports24h/products_index.html', context)


@user_passes_test(seller_check, login_url=reverse_lazy('sports24h:access_denied'))
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


@login_required(login_url=reverse_lazy('sports24h:login_user'))    # TODO permitir apenas seller ter acesso a esta view
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.owner.user == request.user:
        post.delete()
    return HttpResponseRedirect(reverse('sports24h:index'))


def client_check(user):
    return Client.objects.filter(user=user).exists()


def admin_check(user):
    return user.is_superuser or user.is_staff


def access_denied(request):
    return render(request, 'sports24h/accessdenied.html')


@user_passes_test(seller_check, login_url=reverse_lazy('sports24h:access_denied'))
@login_required(login_url=reverse_lazy('sports24h:login_user'))
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
        p = Product.objects.create(owner=seller, name=name, size=s, photo=photo, price=price, forum=f)
        return HttpResponseRedirect(reverse('sports24h:index'))
    else:
        context = {
            'error_message': "Please, check if the fields are correctly filled.",
        }
        return render(request, 'sports24h/product.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))    # TODO permitir apenas seller ter acesso a esta view
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.owner.user == request.use:
        product.delete()
    return HttpResponseRedirect(reverse('sports24h:index'))


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


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    is_owner = Seller.objects.filter(user=request.user).exists()
    average_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    context = {
        'product': product,
        'is_owner': is_owner,
        'average_rating': average_rating
    }
    return render(request, 'sports24h/product_detail.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('owner__user'), pk=post_id)
    comments = Comment.objects.filter(post=post)
    is_owner = Seller.objects.filter(user=request.user).exists()
    context = {
        'post': post,
        'comments': comments,
        'is_owner': is_owner
    }
    return render(request, 'sports24h/post_detail.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def add_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get("comment_text")
        post_id = request.POST.get("post_id")
        post = Post.objects.get(pk=post_id)
        if comment_text.contains('ola') or comment_text.contains('adeus') or comment_text.contains('aqui'):
            context = {
                'error_message': "Please, check if the fields are correctly filled.",
            }
            return render(request, 'sports24h/accessdenied.html', context)

        Comment.objects.create(user=request.user, post=post, text=comment_text)
        return redirect('sports24h:post_detail', post_id=post_id)
    else:
        return redirect('sports24h:index')


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
        context = {
            'country_list': Country.objects.all,
        }
        return render(request, 'sports24h/create_team.html', context)
    name = request.POST.get('name')
    country = request.POST.get('countries')
    if name and country:
        t = Team(name=name, country=country)
        t.save()
        return HttpResponseRedirect(reverse('sports24h:index'))
    else:
        context = {
            'error_message': "Please, check if the fields are correctly filled.",
            'country_list': Country.objects.all,
        }
        return render(request, 'sports24h/create_team.html', context)


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
    name = request.POST.get('forum_name')
    genre = request.POST.get('genre')
    if name and genre:
        Forum.objects.create(name=name, genre=genre)
        return HttpResponseRedirect(reverse('sports24h:forums_index'))
    else:
        context = {
            'error_message': "Please, check if the fields are correctly filled.",
        }
        return render(request, 'sports24h/create_forum.html', context=context)


def register_user(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/register.html')
    passwd = request.POST.get('password')
    confirm_passwd = request.POST.get('confirm_password')

    if passwd != confirm_passwd:
        context = {
            'error_message': "Passwords don't match",
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
            'error_message': "Please, fill all the fields.",
        }
        return render(request, 'sports24h/register.html', context=context)

    if User.objects.filter(username=username).exists():
        context = {
            'error_message': "The username is already in use! Please, choose another one.",
        }
        return render(request, 'sports24h/register.html', context)

    try:
        validate_email(email)
    except ValidationError:
        # Invalid email format
        context = {
            'error_message': "Please introduce a valid e-mail.",
        }
        return render(request, 'sports24h/register.html', context=context)

    if len(passwd) < 8:
        # Password is too short
        context = {
            'error_message': "Password should have at least 8 characters.",
        }
        return render(request, 'sports24h/register.html', context=context)

    birthdate = date.fromisoformat(birthdate_str)
    if (date.today() - birthdate).days < 365 * 18:
        # User is not yet 18 years old
        context = {
            'error_message': "You must be 18 years or older.",
        }
        return render(request, 'sports24h/register.html', context=context)

    u = User.objects.create_user(username=username, email=email, password=passwd)

    if user_type == 'client':
        Client.objects.create(user=u, birthdate=birthdate)
    elif user_type == 'seller':
        Seller.objects.create(user=u, birthdate=birthdate)
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
        if hasattr(request.user, 'client'):
            request.session['photo'] = request.user.client.photo.url
        elif hasattr(request.user, 'seller'):
            request.session['photo'] = request.user.seller.photo.url
        return HttpResponseRedirect(reverse('sports24h:index'))
    else:
        # user doesn't exist
        context = {
            'error_message': "The username doesn't exist in the database!",
        }
        return render(request, 'sports24h/login.html', context)


def logout_user(request):
    if not request.method == 'POST':
        return render(request, 'sports24h/logout.html')
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse('sports24h:login_user'))


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def profile(request):
    if not request.method == 'POST':
        if hasattr(request.user, 'client'):
            c = Client.objects.get(user=request.user)

        elif hasattr(request.user, 'seller'):
            c = Seller.objects.get(user=request.user)
        followers_count = Follows.objects.filter(followed_user=request.user).count()
        context = {
            'nr_followers': followers_count,
            'c': c,
            'countries': Country.objects.all(),
            'teams': Team.objects.all(),
            'sports': Sport.objects.all()
        }
        return render(request, 'sports24h/profile.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def other_user_profile(request, user_id):
    user_information = None
    try:
        user = User.objects.get(pk=user_id)
        if hasattr(user, 'client'):
            user_information = Client.objects.get(user=user)
        elif hasattr(user, 'seller'):
            user_information = Seller.objects.get(user=user)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    followers_count = Follows.objects.filter(followed_user=user).count()
    context = {
        'user': user,
        'user_information': user_information,
        'nr_followers': followers_count
    }
    return render(request, 'sports24h/other_user_profile.html', context)


@login_required(login_url=reverse_lazy('sports24h:login_user'))
def delete_account(request):
    request.user.delete()
    return HttpResponseRedirect(reverse('sports24h:login_user'))


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
        myfile = request.FILES['myfile']
        if Client.objects.filter(user=request.user).exists():
            c = Client.objects.get(user=request.user)
            c.photo.save(myfile.name, myfile)
            c.save()
            request.session['photo'] = c.photo.url
        elif Seller.objects.filter(user=request.user).exists():
            s = Seller.objects.get(user=request.user)
            s.photo.save(myfile.name, myfile)
            s.save()
            request.session['photo'] = s.photo.url

    followers_count = Follows.objects.filter(followed_user=request.user).count()
    context = {
        'nr_followers': followers_count,
        'c': c,
        'countries': Country.objects.all(),
        'teams': Team.objects.all(),
        'sports': Sport.objects.all(),
        'uploaded_file_status': "Photo updated successfully"
    }
    return render(request, 'sports24h/profile.html', context)



@login_required(login_url=reverse_lazy('sports24h:login_user'))
def reset_photo(request):
    user = request.user
    default_photo_path = '/sports24h/static/media/users/default-user-icon.png'
    if hasattr(user, 'client'):
        request.session['photo'] = default_photo_path
        user.client.save()
    elif hasattr(user, 'seller'):
        request.session['photo'] = default_photo_path
        user.seller.save()
    return render(request, 'sports24h/profile.html',
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


@login_required(login_url=reverse_lazy('sports24h:login_user'))     # TODO fazer isto acesssivel apenas a users com @client
def add_to_cart(request, product_id):
    if not hasattr(request.user, 'client'):
        return HttpResponseRedirect(reverse('sports24h:index'))

    client = Client.objects.get(user=request.user)
    try:
        shopping_cart = ShoppingCart.objects.get(client=client)
    except ObjectDoesNotExist:
        shopping_cart = ShoppingCart.objects.create(client=client)

    product = Product.objects.get(id=product_id)
    shopping_cart.product_list.add(product)

    return HttpResponseRedirect(reverse('sports24h:index'))


def remove_from_cart(request, product_id):
    client = Client.objects.get(user=request.user)
    shopping_cart = ShoppingCart.objects.get(client=client)
    product = Product.objects.get(id=product_id)
    shopping_cart.product_list.remove(product)

    return HttpResponseRedirect(reverse('sports24h:shopping_cart'))


def send_message_html(request):
    messages_list = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    paginator = Paginator(messages_list, 10)  # Show 10 messages per page

    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)

    return render(request, 'sports24h/send_message.html', {'messages': messages})


def sent_messages_html(request):
    messages_list = Message.objects.filter(sender=request.user).order_by('-sent_at')
    paginator = Paginator(messages_list, 10)  # Show 10 messages per page

    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)

    return render(request, 'sports24h/sent_messages.html', {'messages': messages})


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
            return redirect('sports24h:index')
        except User.DoesNotExist:
            return render(request, 'sports24h/send_message.html', {'error': 'Destinatário não encontrado'})

    return render(request, 'sports24h/send_message.html')


def like(request, post_id):          # TODO restringir a instancias de clientes apenas
    post = Post.objects.get(pk=post_id)
    try:
        like = Likes.objects.get(user=request.user, post=post)
        like.delete()
        post.likes_count -= 1
    except ObjectDoesNotExist:
        Likes.objects.create(user=request.user, post=post)
        post.likes_count += 1
    post.save()
    return redirect(request.META['HTTP_REFERER'])


@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('sports24h:login_user'))
def admin(request):
    return render(request, 'sports24h/admin_options.html')


#### VIEWS REACT
@api_view(['GET', 'POST'])  # (3)
def post_list(request):
    if request.method == 'GET':  # (4)
        posts = Post.objects.all()
        serializerP = PostSerializer(posts, context={'request': request}, many=True)
        return Response(serializerP.data)
    elif request.method == 'POST':  # (4)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def post_edita(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])  # (3)
def comment_list(request):
    if request.method == 'GET':  # (4)
        comments = Comment.objects.all()
        serializerC = CommentSerializer(comments, context={'request': request}, many=True)
        return Response(serializerC.data)
    elif request.method == 'POST':  # (4)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
