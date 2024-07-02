# Generated by Django 4.2.9 on 2024-01-12 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('release_date', models.DateField(verbose_name='发表时间')),
                ('description', models.TextField(verbose_name='文案')),
            ],
            options={
                'verbose_name_plural': '3.专辑管理',
            },
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('formation_date', models.DateField(verbose_name='成立时间')),
                ('introduction', models.TextField(verbose_name='介绍')),
                ('member_count', models.IntegerField(blank=True, default=0, null=True, verbose_name='成员人数')),
            ],
            options={
                'verbose_name_plural': '1.乐队管理',
            },
        ),
        migrations.CreateModel(
            name='Fan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('gender', models.CharField(max_length=10, verbose_name='性别')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('occupation', models.CharField(max_length=50, verbose_name='职业')),
                ('education', models.CharField(max_length=50, verbose_name='学历')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '6.粉丝管理',
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('authors', models.CharField(max_length=100, verbose_name='词曲作者')),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.album', verbose_name='专辑ID')),
            ],
            options={
                'verbose_name_plural': '4.歌曲管理',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='评论')),
                ('rating', models.FloatField(verbose_name='打分')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.album', verbose_name='专辑ID')),
                ('fan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.fan', verbose_name='歌迷ID')),
            ],
            options={
                'verbose_name_plural': '7.评论管理',
            },
        ),
        migrations.CreateModel(
            name='LikedSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.fan', verbose_name='歌迷')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.song', verbose_name='歌曲')),
            ],
            options={
                'verbose_name_plural': '喜欢的歌曲',
            },
        ),
        migrations.CreateModel(
            name='LikedBand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.band', verbose_name='乐队')),
                ('fan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.fan', verbose_name='歌迷')),
            ],
            options={
                'verbose_name_plural': '8.喜欢的乐队',
            },
        ),
        migrations.CreateModel(
            name='LikedAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.album', verbose_name='专辑')),
                ('fan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.fan', verbose_name='歌迷')),
            ],
            options={
                'verbose_name_plural': '9.喜欢的专辑',
            },
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('date', models.DateField(verbose_name='举办时间')),
                ('location', models.CharField(max_length=100, verbose_name='地点')),
                ('band', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.band', verbose_name='乐队ID')),
            ],
            options={
                'verbose_name_plural': '5.演唱会管理',
            },
        ),
        migrations.CreateModel(
            name='BandMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('gender', models.CharField(max_length=10, verbose_name='性别')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('role', models.CharField(max_length=50, verbose_name='分工')),
                ('join_date', models.DateField(verbose_name='加入时间')),
                ('leave_date', models.DateField(blank=True, default=None, null=True, verbose_name='离开时间')),
                ('band', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.band', verbose_name='乐队ID')),
            ],
            options={
                'verbose_name_plural': '2.乐队成员管理',
            },
        ),
        migrations.AddField(
            model_name='band',
            name='captain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='captain', to='app.bandmember', verbose_name='队长'),
        ),
        migrations.AddField(
            model_name='band',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.concert', verbose_name='演唱会')),
                ('fan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.fan', verbose_name='歌迷')),
            ],
            options={
                'verbose_name_plural': '参加的演唱会',
            },
        ),
        migrations.AddField(
            model_name='album',
            name='band',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.band', verbose_name='乐队ID'),
        ),
    ]