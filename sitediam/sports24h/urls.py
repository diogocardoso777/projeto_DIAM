from django.urls import include, path
from . import views

# (. significa que importa views da mesma directoria)
app_name = 'sports24h'

urlpatterns = [
    path("", views.index, name="index"),

    path("posts_index", views.posts_index, name="posts_index"),

    path("products_index", views.products_index, name="products_index"),

    path("register", views.register_user, name="register_user"),

    path("login", views.login_user, name="login_user"),

    path("logout", views.logout_user, name="logout_user"),

    path("forums", views.forums_index, name="forums_index"),

    path("follow_forum", views.follow_forum, name="follow_forum"),

    # create forum
    path("create_forum", views.forum, name="create_forum"),

    path("create_post", views.post, name="create_post"),

    path("delete_post", views.delete_post, name="delete_post"),

    # post/1  - detail
    path("post/<int:post_id>", views.post_detail, name="post_detail"),

    path("add_comment", views.add_comment, name="add_comment"),

    path("create_product", views.product, name="create_product"),

    path("delete_product", views.delete_product, name="delete_product"),

    # product/1  - detail
    path("product/<int:product_id>", views.product_detail, name="product_detail"),

    # add to cart
    path("add_to_cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),

    path("remove_from_cart/<int:product_id>", views.remove_from_cart, name="remove_from_cart"),

    # seller products
    path('seller_products', views.seller_products, name='seller_products'),

    #admin views
    #path("create_country", views., name="create_product"),

    path("create_country", views.country, name="create_country"),

    path("create_size", views.size, name="create_size"),

    path("create_sport", views.sport, name="create_sport"),

    path("create_team", views.team, name="create_team"),

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
    path('reset_photo', views.reset_photo, name='reset_photo'),

    # shopping cart
    path('shopping_cart', views.shopping_cart, name='shopping_cart'),

    # send messages
    path('send_message/', views.send_message_html, name='send_message_html'),
    path('send_message/submit/', views.send_message_submit, name='send_message_submit'),

    #receive messages
    path('send_message/', views.inbox, name='receive_message'),

    #sent messages
    path('sent_messages/', views.sent_messages_html, name='sent_messages_html'),

    # like post
    path('like/<int:post_id>', views.like, name='like'),

    # about
    path('about/', views.about_index, name='about_index'),

    path('search_users', views.search_users, name='search_users'),

    path('follow_user', views.follow_user, name='follow_user'),

    path('unfollow_user', views.unfollow_user, name='unfollow_user'),

    path('admin', views.admin, name='admin'),

    path('acess_denied', views.access_denied, name='access_denied'),

    path('delete_account', views.delete_account, name='delete_account'),

    path('api/posts/', views.post_list),
    path('api/posts/<int:pk>', views.post_detail),
    path('api/comments/', views.comment_list),

]
