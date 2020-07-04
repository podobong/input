from django.db import models


class Univ(models.Model):
    class Meta:
        verbose_name = '대학'
        verbose_name_plural = '대학'

    name = models.CharField(
            verbose_name='대학명',
            unique=True,
            max_length=30,
    )
    logo = models.ImageField(
            verbose_name='로고 이미지',
            blank=True,
    )
    review_url = models.CharField(
            verbose_name='리뷰 URL',
            blank=True,
            max_length=100,
    )

    def __str__(self):
        return self.name


class SusiJH(models.Model):
    class Meta:
        verbose_name = '수시전형'
        verbose_name_plural = '수시전형'

    univ = models.ForeignKey(
            verbose_name='대학',
            to=Univ,
            related_name='susi_jhs',
            on_delete=models.CASCADE,
    )
    name = models.CharField(
            verbose_name='전형명',
            max_length=30,
    )

    def __str__(self):
        return f'{self.univ.name}|{self.name}'


class SusiMajor(models.Model):
    class Meta:
        verbose_name = '수시 학과'
        verbose_name_plural = '수시 학과'

    susi_jh = models.ForeignKey(
            verbose_name='수시전형',
            to=SusiJH,
            related_name='susi_majors',
            on_delete=models.CASCADE,
            )
    name = models.CharField(
            verbose_name='학과명',
            max_length=50,
            )

    def __str__(self):
        return f'{self.susi_jh.univ.name}|{self.susi_jh.name}|{self.name}'


class SusiSchedule(models.Model):
    class Meta:
        verbose_name = '수시 일정'
        verbose_name_plural = '수시 일정'

    major = models.ForeignKey(
            verbose_name='수시 학과',
            to=SusiMajor,
            related_name='susi_schedules',
            on_delete=models.CASCADE,
    )
    description = models.CharField(
            verbose_name='일정 설명',
            max_length=255,
    )
    start_date = models.DateTimeField(
            verbose_name='시작 시간',
    )
    end_date = models.DateTimeField(
            verbose_name='종료 시간',
    )

    def __str__(self):
        return f'{self.major.susi_jh.univ.name}|{self.major.susi_jh.name}|{self.major.name}|{self.description}'


class Device(models.Model):
    class Meta:
        verbose_name = '기기 정보'
        verbose_name_plural = '기기 정보'

    unique_id = models.CharField(
            verbose_name='기기 ID',
            max_length=50,
            )
    susis = models.ManyToManyField(
            verbose_name='즐찾 수시',
            to=SusiMajor,
            related_name='devices',
            )

    def __str__(self):
        return self.unique_id

