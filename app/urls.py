from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.user_login),
    # path('register/', views.user_register),
    path('logout/', views.user_logout),

    path('my_band/', views.my_band, name='my_band'),
    path('band/member/', views.band_member, name='band_member'),
    path('band/member/edit/<int:member_id>', views.band_member_edit, name='band_member_edit'),
    path('band/member/delete/<int:member_id>', views.band_member_delete, name='band_member_delete'),

    path('band/album/', views.band_album, name='band_album'),
    path('band/album/edit/<int:album_id>', views.band_album_edit, name='band_album_edit'),
    path('band/album/delete/<int:album_id>', views.band_album_delete, name='band_album_delete'),

    path('band/concert/', views.band_concert, name='band_concert'),
    path('band/concert/edit/<int:concert_id>', views.band_concert_edit, name='band_concert_edit'),
    path('band/concert/delete/<int:concert_id>', views.band_concert_delete, name='band_concert_delete'),

    path('album/song/<int:album_id>', views.album_song, name='album_song'),
    path('album/song/edit/<int:song_id>', views.album_song_edit, name='album_song_edit'),
    path('album/song/delete/<int:song_id>', views.album_song_delete, name='album_song_delete'),
    path('album/review/<int:album_id>', views.album_review, name='album_review'),
    path('album/fan/<int:album_id>', views.album_fan, name='album_fan'),

    path('band/fan', views.band_fan, name='fan'),
    path('band/fan_statistics', views.fan_statistics, name='fan_statistics'),
    path('song/fan/<int:song_id>', views.song_fan, name='song_fan'),
    path('concert/fan/<int:concert_id>', views.concert_fan, name='concert_fan'),

    path('fan/', views.fan_index, name='fan'),
    path('fan/band/', views.fan_band, name='fan_band'),
    path('fan/album/', views.fan_album),
    path('fan/song/', views.fan_song),
    path('fan/concert/', views.fan_concert),

    path('fan/band/<int:band_id>', views.fan_band_detail),
    path('fan/album/<int:album_id>', views.fan_album_detail),
    path('fan/song/<int:song_id>', views.fan_song_detail),
    path('fan/concert/<int:concert_id>', views.fan_concert_detail),
    path('fan/add_review/<int:album_id>', views.fan_add_review),

    path('my_like', views.my_like),

    path('fan/like_band/<int:band_id>', views.fan_like_band),
    path('fan/like_album/<int:album_id>', views.fan_like_album),
    path('fan/like_song/<int:song_id>', views.fan_like_song),
    path('fan/attend_concert/<int:concert_id>', views.fan_attend_concert),
    path('fan/info/', views.fan_info)

]
