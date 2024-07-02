import time
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.db.models import Q, Count, Avg
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
import datetime
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)
from .models import *


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = auth.authenticate(username=username, password=password)
        if user:

            if user_type == '歌迷':
                if Fan.objects.filter(user=user):
                    auth.login(request, user)
                    return HttpResponseRedirect('/app/fan/')
                else:
                    pass
            elif user_type == '乐队':
                if Band.objects.filter(user=user):
                    auth.login(request, user)
                    return HttpResponseRedirect('/app/my_band/')
                else:
                    pass
            else:
                if user.is_superuser:
                    auth.login(request, user)
                    return HttpResponseRedirect('/admin')
                else:
                    pass

            return render(request, 'login.html', {"error": "该用户不是{}".format(user_type)})

        else:
            return render(request, 'login.html', {"error": "用户名或密码错误"})


@login_required()
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/app/login/')


@login_required()
def my_band(request):
    band = Band.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        formation_date = request.POST.get('formation_date')
        introduction = request.POST.get('introduction')
        captain = request.POST.get('captain')
        band.name = name
        band.formation_date = formation_date
        band.introduction = introduction
        band.captain_id = captain
        band.save()
        return redirect(my_band)

    return render(request, 'band/band.html', {'band': band})


def band_member(request):
    band = Band.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        gener = request.POST.get('gender')
        age = request.POST.get('age')
        role = request.POST.get('role')
        join_date = request.POST.get('join_date')

        BandMember.objects.create(name=name, gender=gener, age=age, role=role, join_date=join_date, band=band)

    members = BandMember.objects.filter(band_id=band.id)
    return render(request, 'band/member.html', {'members': members, 'band': band})


def band_member_edit(request, member_id):
    if request.method == 'POST':
        # Get and update member information
        print(request.POST)
        member = BandMember.objects.get(pk=member_id)
        member.name = request.POST.get('member_name')
        member.gender = request.POST.get('gender')
        member.age = request.POST.get('age')
        member.role = request.POST.get('role')
        member.join_date = request.POST.get('join_date')
        if request.POST.get('leave_date', None):
            member.leave_date = request.POST.get('leave_date', None)

        member.save()
        messages.success(request, '修改成功')
        return redirect(band_member)


def band_member_delete(request, member_id):
    member = BandMember.objects.get(pk=member_id)
    member.band = None
    member.leave_date = datetime.date.today()
    member.save()
    messages.success(request, '成员离队成功')
    return redirect('band_member')


def band_album(request):
    band = Band.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('album_name')
        release_date = request.POST.get('release_date')
        description = request.POST.get('description')

        Album.objects.create(name=name, release_date=release_date, description=description, band=band)

    albums = Album.objects.filter(band_id=band.id)  # Replace '1' with the appropriate band ID

    for album in albums:
        album.average_rating = round(Review.objects.filter(album_id=album.id).aggregate(Avg('rating'))['rating__avg'],
                                     1)
    return render(request, 'band/album.html', {'albums': albums, 'band': band})


def band_album_edit(request, album_id):
    if request.method == 'POST':
        print(request.POST)
        album = Album.objects.get(pk=album_id)
        album.name = request.POST.get('album_name')
        album.release_date = request.POST.get('release_date')
        album.description = request.POST.get('description')

        album.save()
        messages.success(request, '修改成功')
        return redirect('band_album')


def band_album_delete(request, album_id):
    Album.objects.get(pk=album_id).delete()
    messages.success(request, '专辑删除成功')
    return redirect('band_album')


def album_review(request, album_id):
    album = Album.objects.get(pk=album_id)
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title')
        content = request.POST.get('content')
        rating = request.POST.get('rating')

        Review.objects.create(title=title, content=content, rating=rating, album=album)

    reviews = Review.objects.filter(album_id=album_id)
    return render(request, 'band/review.html', {'comments': reviews, 'album': album})


def album_fan(request, album_id):
    fans = Fan.objects.filter(likedalbum__album_id=album_id)
    album = Album.objects.get(pk=album_id)
    title = '喜欢《{}》的粉丝'.format(album.name)
    return render(request, 'band/fan.html', {'fans': fans, 'album': album, 'title': title})


def band_concert(request):
    band = Band.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('concert_name')
        date = request.POST.get('date')
        location = request.POST.get('location')

        Concert.objects.create(name=name, date=date, location=location, band=band)

    concerts = Concert.objects.filter(band_id=band.id)  # Replace '1' with the appropriate band ID
    return render(request, 'band/concert.html', {'concerts': concerts, 'band': band})


def band_concert_edit(request, concert_id):
    if request.method == 'POST':
        print(request.POST)
        concert = Concert.objects.get(pk=concert_id)
        concert.name = request.POST.get('concert_name')
        concert.date = request.POST.get('date')
        concert.location = request.POST.get('location')

        concert.save()
        messages.success(request, '修改成功')
        return redirect('band_concert')


def band_concert_delete(request, concert_id):
    Concert.objects.get(pk=concert_id).delete()
    messages.success(request, '演唱会删除成功')
    return redirect('band_concert')


def album_song(request, album_id):
    album = Album.objects.get(pk=album_id)
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('song_name')
        authors = request.POST.get('authors')

        Song.objects.create(name=name, authors=authors, album=album)

    songs = Song.objects.filter(album_id=album_id)
    return render(request, 'band/song.html', {'songs': songs, 'album': album})


def album_song_edit(request, song_id):
    if request.method == 'POST':
        print(request.POST)
        song = Song.objects.get(pk=song_id)
        song.name = request.POST.get('song_name')
        song.authors = request.POST.get('authors')

        song.save()
        messages.success(request, '修改成功')
        return redirect('album_song', album_id=song.album_id)


def album_song_delete(request, song_id):
    band_id = Song.objects.get(pk=song_id).album.band_id
    Song.objects.get(pk=song_id).delete()
    messages.success(request, '歌曲删除成功')
    return redirect('album_song', album_id=band_id)


def band_fan(request):
    band = Band.objects.get(user=request.user)
    print(band.id)
    fans = Fan.objects.filter(likedband__band_id=band.id)
    print(fans)
    title = '乐队粉丝'
    return render(request, 'band/fan.html', {'fans': fans, 'band': band, 'title': title})


from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar
from .models import Fan


def fan_statistics(request):
    fans = Fan.objects.all()

    band = Band.objects.get(user=request.user)
    # 统计性别占比
    gender_counts = dict(
        Fan.objects.filter(likedband__band=band).values('gender').annotate(count=models.Count('id')).values_list(
            'gender',
            'count'))

    print(gender_counts)
    gender_pie = (
        Pie()
        .add("", list(gender_counts.items()))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .set_global_opts(title_opts=opts.TitleOpts(title="粉丝性别分布"))
    )

    # 统计职业占比
    occupation_counts = dict(
        Fan.objects.filter(likedband__band=band).values('occupation').annotate(count=models.Count('id')).values_list(
            'occupation', 'count'))

    occupation_pie = (
        Pie()
        .add("", list(occupation_counts.items()))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .set_global_opts(title_opts=opts.TitleOpts(title="粉丝职业分布"))
    )

    # 统计学历占比
    education_counts = dict(
        Fan.objects.filter(likedband__band=band).values('education').annotate(count=models.Count('id')).values_list(
            'education', 'count'))
    education_pie = (
        Pie()
        .add("", list(education_counts.items()))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .set_global_opts(title_opts=opts.TitleOpts(title="粉丝学历分布"))
    )

    # 将图表以 HTML 字符串传递给前端页面
    gender_pie_html = gender_pie.render_embed()
    occupation_pie_html = occupation_pie.render_embed()
    education_pie_html = education_pie.render_embed()

    return render(
        request,
        'band/fan_statistics.html',
        context={
            'gender_pie_html': gender_pie_html,
            'occupation_pie_html': occupation_pie_html,
            'education_pie_html': education_pie_html,
        }
    )


def song_fan(request, song_id):
    fans = Fan.objects.filter(likedsong__song_id=song_id)
    song = Song.objects.get(pk=song_id)
    title = '喜欢《{}》歌曲的粉丝'.format(song.name)
    return render(request, 'band/fan.html', {'fans': fans, 'song': song, 'title': title})


def concert_fan(request, concert_id):
    fans = Fan.objects.filter(attendance__concert_id=concert_id)
    concert = Concert.objects.get(pk=concert_id)
    title = '参加《{}》演唱会的粉丝'.format(concert.name)
    return render(request, 'band/fan.html', {'fans': fans, 'concert': concert, 'title': title})


def fan_band(request):
    keyword = request.GET.get('keyword')
    if not keyword:
        band = Band.objects.all()
    else:
        band = Band.objects.filter(Q(name__icontains=keyword))
    return render(request, 'fan/band.html', {'bands': band, 'keyword': keyword})


def fan_album(request):
    keyword = request.GET.get('keyword')
    if not keyword:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(Q(name__icontains=keyword) | Q(band__name__icontains=keyword))

    for album in albums:
        album.average_rating = round(Review.objects.filter(album_id=album.id).aggregate(Avg('rating'))['rating__avg'],
                                     1)
    return render(request, 'fan/album.html', {'albums': albums, 'keyword': keyword})


def fan_concert(request):
    keyword = request.GET.get('keyword')
    if not keyword:
        concerts = Concert.objects.all()
    else:
        concerts = Concert.objects.filter(Q(name__icontains=keyword) | Q(band__name__icontains=keyword))
    return render(request, 'fan/concert.html', {'concerts': concerts, 'keyword': keyword})


def fan_song(request):
    keyword = request.GET.get('keyword')
    if not keyword:
        songs = Song.objects.all()
    else:
        songs = Song.objects.filter(name__icontains=keyword)
    return render(request, 'fan/song.html', {'songs': songs, 'keyword': keyword})


def my_like(request):
    fan = Fan.objects.get(user=request.user)
    bands = Band.objects.filter(likedband__fan=fan)
    albums = Album.objects.filter(likedalbum__fan=fan)
    songs = Song.objects.filter(likedsong__fan=fan)
    concerts = Concert.objects.filter(attendance__fan=fan)
    for album in albums:
        album.average_rating = round(Review.objects.filter(album_id=album.id).aggregate(Avg('rating'))['rating__avg'],
                                     1)
    return render(request, 'fan/my_like.html',
                  {'bands': bands, 'fan': fan, 'albums': albums, 'songs': songs, 'concerts': concerts})


def fan_band_detail(request, band_id):
    band = Band.objects.get(pk=band_id)
    if LikedBand.objects.filter(band_id=band_id, fan__user=request.user):
        band.like = True
    else:
        band.like = False
    return render(request, 'fan/band_detail.html', {'band': band})


def fan_album_detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.average_rating = round(Review.objects.filter(album_id=album.id).aggregate(Avg('rating'))['rating__avg'],
                                 1)
    comments = Review.objects.filter(album_id=album_id).order_by('-create_time')
    if LikedAlbum.objects.filter(album_id=album_id, fan__user=request.user):
        album.like = True
    else:
        album.like = False

    if Review.objects.filter(album_id=album_id, fan__user=request.user):
        album.review = True
    else:
        album.review = False
    return render(request, 'fan/album_detail.html', {'album': album, 'comments': comments})


def fan_concert_detail(request, concert_id):
    concert = Concert.objects.get(pk=concert_id)
    if Attendance.objects.filter(concert_id=concert_id, fan__user=request.user):
        concert.attend = True
    else:
        concert.attend = False
    return render(request, 'fan/concert_detail.html', {'concert': concert})


def fan_song_detail(request, song_id):
    song = Song.objects.get(pk=song_id)
    if LikedSong.objects.filter(song_id=song_id, fan__user=request.user):
        song.like = True
    else:
        song.like = False
    return render(request, 'fan/song_detail.html', {'song': song})


def fan_index(request):
    return redirect('fan_band')


def fan_add_review(request, album_id):
    fan = Fan.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        if not Review.objects.filter(album_id=album_id, fan=fan):
            Review.objects.create(comment=content, rating=rating, album_id=album_id, fan=fan)
        else:
            messages.error(request, '您已经评价过了')
        return redirect('/app/fan/album/{}'.format(album_id))


def fan_like_band(request, band_id):
    fan = Fan.objects.get(user=request.user)
    band = Band.objects.get(pk=band_id)
    if LikedBand.objects.filter(band_id=band_id, fan__user=request.user):
        LikedBand.objects.get(band_id=band_id, fan__user=request.user).delete()
    else:
        LikedBand.objects.create(band=band, fan=fan)
    return JsonResponse({'status': 'success'})


def fan_like_album(request, album_id):
    fan = Fan.objects.get(user=request.user)
    album = Album.objects.get(pk=album_id)
    if LikedAlbum.objects.filter(album_id=album_id, fan__user=request.user):
        LikedAlbum.objects.get(album_id=album_id, fan__user=request.user).delete()
    else:
        LikedAlbum.objects.create(album=album, fan=fan)
    return JsonResponse({'status': 'success'})


def fan_like_song(request, song_id):
    fan = Fan.objects.get(user=request.user)
    song = Song.objects.get(pk=song_id)
    if LikedSong.objects.filter(song_id=song_id, fan__user=request.user):
        LikedSong.objects.get(song_id=song_id, fan__user=request.user).delete()
    else:
        LikedSong.objects.create(song=song, fan=fan)
    return JsonResponse({'status': 'success'})


def fan_attend_concert(request, concert_id):
    fan = Fan.objects.get(user=request.user)
    concert = Concert.objects.get(pk=concert_id)
    if Attendance.objects.filter(concert_id=concert_id, fan__user=request.user):
        Attendance.objects.get(concert_id=concert_id, fan__user=request.user).delete()
    else:
        Attendance.objects.create(concert=concert, fan=fan)
    return JsonResponse({'status': 'success'})


def fan_info(request):
    fan = Fan.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        occupation = request.POST.get('occupation')
        education = request.POST.get('education')
        fan.name = name
        fan.gender = gender
        fan.age = age
        fan.occupation = occupation
        fan.education = education
        fan.save()

    context = {'fan': fan}
    return render(request, 'fan/fan.html', context)
