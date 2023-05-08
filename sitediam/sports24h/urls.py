from django.urls import include, path
from . import views

# (. significa que importa views da mesma directoria)
app_name = 'sports24h'

urlpatterns = [
    path("", views.index, name="index"),

    path("register", views.register_user, name="register_user"),

    path("login", views.login_user, name="login_user"),

    path("logout", views.logout_user, name="logout_user"),

    path("create_post", views.post, name="create_post"),

    path("forums", views.forums_index, name="forums_index"),

    # create forum
    path("create_forum", views.forum, name="create_forum"),

    # user profile
    path("profile", views.profile, name="profile"),

    # upload photo
    path('upload_photo', views.upload_photo, name='upload_photo'),

    # set country
    path('set_country', views.set_country, name='set_country'),

    # set favoriteTeam
    path('set_favoriteTeam', views.set_favoriteTeam, name='set_favoriteTeam'),

    # set favoriteSport
    path('set_favoriteSport', views.set_favoriteSport, name='set_favoriteSport'),
    # reset foto
    path('reset_foto', views.reset_foto, name='reset_foto'),

    # shopping cart
    path('shopping_cart', views.shopping_cart, name='shopping_cart'),

    #
]
