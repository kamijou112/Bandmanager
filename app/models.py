from django.db import models


class Band(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='名称')
    formation_date = models.DateField(verbose_name='成立时间')
    introduction = models.TextField(verbose_name='介绍')
    captain = models.ForeignKey('BandMember', on_delete=models.CASCADE, verbose_name='队长', null=True, blank=True,
                                related_name='captain')
    member_count = models.IntegerField(default=0, verbose_name='成员人数', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '1.乐队管理'


class BandMember(models.Model):
    GENDER_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    role = models.CharField(max_length=50, verbose_name='分工')
    join_date = models.DateField(verbose_name='加入时间')
    leave_date = models.DateField(null=True, blank=True, verbose_name='离开时间', default=None)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, verbose_name='乐队ID', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Update member_count when saving a new member
        super().save(*args, **kwargs)
        if self.band:
            self.band.member_count = self.band.bandmember_set.count()
            self.band.save()

    def delete(self, *args, **kwargs):
        # Update member_count when deleting a member
        band = self.band
        super().delete(*args, **kwargs)
        if band:
            band.member_count = band.bandmember_set.count()
            band.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '2.乐队成员管理'


class Album(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    release_date = models.DateField(verbose_name='发表时间')
    description = models.TextField(verbose_name='文案')
    band = models.ForeignKey(Band, on_delete=models.CASCADE, verbose_name='乐队ID', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '3.专辑管理'


class Song(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    authors = models.CharField(max_length=100, verbose_name='词曲作者')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='专辑ID', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '4.歌曲管理'


class Concert(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    date = models.DateField(verbose_name='举办时间')
    location = models.CharField(max_length=100, verbose_name='地点')
    band = models.ForeignKey(Band, on_delete=models.CASCADE, null=True, blank=True, verbose_name='乐队ID')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '5.演唱会管理'


class Fan(models.Model):
    GENDER_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]

    EDUCATION_CHOICES = [
        ('小学', '小学'),
        ('初中', '初中'),
        ('高中', '高中'),
        ('大学', '大学'),
        ('硕士', '硕士'),
        ('博士', '博士'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    occupation = models.CharField(max_length=50, verbose_name='职业')
    education = models.CharField(max_length=50, choices=EDUCATION_CHOICES, verbose_name='学历')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '6.粉丝管理'


class Review(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, verbose_name='歌迷')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='专辑')
    comment = models.TextField(verbose_name='评论')
    rating = models.FloatField(verbose_name='打分')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)

    class Meta:
        verbose_name_plural = '7.评论管理'

    def __str__(self):
        return self.fan.name + '对' + self.album.name + '的评论'


class LikedBand(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, verbose_name='歌迷')
    band = models.ForeignKey(Band, on_delete=models.CASCADE, verbose_name='乐队')

    class Meta:
        verbose_name_plural = '8.喜欢的乐队'

    def __str__(self):
        return self.fan.name + '喜欢' + self.band.name


class LikedAlbum(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, verbose_name='歌迷')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='专辑')

    def __str__(self):
        return f"{self.fan.name}喜欢{self.album.name}"

    class Meta:
        verbose_name_plural = '9.喜欢的专辑'


class LikedSong(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, verbose_name='歌迷')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name='歌曲')

    def __str__(self):
        return f"{self.fan.name}喜欢{self.song.name}"

    class Meta:
        verbose_name_plural = '喜欢的歌曲'


class Attendance(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, verbose_name='演唱会')
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, verbose_name='歌迷')

    def __str__(self):
        return f"{self.fan.name}参加了{self.concert.name}"

    class Meta:
        verbose_name_plural = '参加的演唱会'
