from datetime import datetime
from django.db import models


SUSI_JEONGSI = (('수시', '수시'), ('정시', '정시'))
YEARS = [(y, y) for y in range(2021, (datetime.now().year+2))]


class University(models.Model):
    class Meta:
        verbose_name = '대학'
        verbose_name_plural = '대학'

    name = models.CharField(
            verbose_name='대학명',
            unique=True,
            max_length=63,
    )
    logo = models.ImageField(
            verbose_name='로고 이미지',
            blank=True,
    )
    review_url = models.CharField(
            verbose_name='리뷰 URL',
            blank=True,
            max_length=127,
    )

    def __str__(self):
        return self.name


class MajorBlock(models.Model):
    class Meta:
        verbose_name = '학과 블록'
        verbose_name_plural = '학과 블록'

    university = models.ForeignKey(
            verbose_name='대학',
            to=University,
            related_name='major_blocks',
            on_delete=models.CASCADE,
    )
    susi_jeongsi = models.CharField(
            verbose_name='수시/정시',
            choices=SUSI_JEONGSI,
            max_length=7,
    )
    name = models.CharField(
            verbose_name='분류명',
            max_length=255,
    )

    def __str__(self):
        return f'{self.university.name}|{self.name}'


class Jeonhyeong(models.Model):
    class Meta:
        verbose_name = '전형'
        verbose_name_plural = '전형'

    university = models.ForeignKey(
            verbose_name='대학',
            to=University,
            related_name='jeonhyeongs',
            on_delete=models.CASCADE,
    )
    susi_jeongsi = models.CharField(
            verbose_name='수시/정시',
            choices=SUSI_JEONGSI,
            max_length=7,
    )
    year = models.IntegerField(
            verbose_name='학년도',
            choices=YEARS,
    )
    name = models.CharField(
            verbose_name='전형명',
            max_length=63,
    )

    def __str__(self):
        return f'{str(self.year)}|{self.university.name}|{self.susi_jeongsi}|{self.name}'


class Schedule(models.Model):
    class Meta:
        verbose_name = '일정'
        verbose_name_plural = '일정'

    jeonhyeong = models.ForeignKey(
            verbose_name='전형',
            to=Jeonhyeong,
            related_name='schedules',
            on_delete=models.CASCADE,
    )
    major_block = models.ForeignKey(
            verbose_name='학과 블록',
            to=MajorBlock,
            related_name='schedules',
            on_delete=models.CASCADE,
    )

    university = models.CharField(
            max_length=63,
            editable=False,
    )
    year = models.IntegerField(
            editable=False,
    )
    sj = models.CharField(
            max_length=7,
            editable=False,
    )
    jh = models.CharField(
            max_length=63,
            editable=False,
    )
    block = models.CharField(
            max_length=255,
            editable=False,
    )

    description = models.CharField(
            verbose_name='설명',
            max_length=255,
    )
    start_date = models.DateTimeField(
            verbose_name='시작시간',
    )
    end_date = models.DateTimeField(
            verbose_name='종료시간',
    )

    def save(self, **kwargs):
        self.university = self.jeonhyeong.university.name
        self.year = self.jeonhyeong.year
        self.sj = self.jeonhyeong.susi_jeongsi
        self.jh = self.jeonhyeong.name
        self.block = self.major_block.name
        super().save()

    def __str__(self):
        return f'{str(self.year)}|{self.university}|{self.susi_jeongsi}|{self.jeonhyeong}|{self.description}|{self.major_block}'

