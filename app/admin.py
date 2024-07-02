from django.contrib import admin
from .models import *


class CustomAdminSite(admin.AdminSite):
    index_template = 'admin/custom_index.html'


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'formation_date', 'captain', 'member_count']
    search_fields = ['name', 'captain_id']
    list_filter = ['formation_date']
    # Add other customizations as needed


@admin.register(BandMember)
class BandMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'age', 'role', 'join_date', 'leave_date', 'band_id']
    search_fields = ['name', 'band_id__name']
    list_filter = ['gender', 'role', 'join_date', 'leave_date']
    # Add other customizations as needed


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'release_date', 'band_id']
    search_fields = ['name', 'band_id__name']
    list_filter = ['release_date']
    # Add other customizations as needed


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'authors', 'album_id']
    search_fields = ['name', 'album_id__name']
    list_filter = ['authors']
    # Add other customizations as needed


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location', 'band_id']
    search_fields = ['name', 'band_id__name']
    list_filter = ['date']
    # Add other customizations as needed


@admin.register(Fan)
class FanAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'age', 'occupation', 'education']
    search_fields = ['name']
    list_filter = ['gender', 'occupation']
    # Add other customizations as needed


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['fan', 'album', 'comment', 'rating']
    search_fields = ['fan__name', 'album__name']
    list_filter = ['rating']
    # Add other customizations as needed


@admin.register(LikedBand)
class LikedBandAdmin(admin.ModelAdmin):
    list_display = ['fan', 'band']
    search_fields = ['fan__name', 'band__name']
    # Add other customizations as needed


@admin.register(LikedAlbum)
class LikedAlbumAdmin(admin.ModelAdmin):
    list_display = ['fan', 'album']
    search_fields = ['fan__name', 'album__name']
    # Add other customizations as needed


@admin.register(LikedSong)
class LikedSongAdmin(admin.ModelAdmin):
    list_display = ['fan', 'song']
    search_fields = ['fan__name', 'song__name']
    # Add other customizations as needed


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['fan', 'concert']
    search_fields = ['fan__name', 'concert__name']
    # Add other customizations as needed
