from django.db import models


SUSI_JEONGSI = (('수시', '수시'), ('정시', '정시'))


class Univ(models.Model):
    class Meta:
        verbose_name = '대학'
        verbose_name_plural = '대학'

    name = models.CharField(
            verbose_name='대학명',
            unique=True,
            max_length=30,
            )
    logo = models.CharField(
            verbose_name='로고 URL',
            blank=True,
            max_length=100,
            )
    review_url = models.CharField(
            verbose_name='리뷰 URL',
            blank=True,
            max_length=100,
            )

    def __str__(self):
        return self.name


class SJ(models.Model):
    class Meta:
        verbose_name = '수시/정시'
        verbose_name_plural = '수시/정시'

    univ = models.ForeignKey(
            verbose_name='대학',
            to=Univ,
            related_name='sjs',
            on_delete=models.CASCADE,
            )
    sj = models.CharField(
            verbose_name='수시/정시',
            choices=SUSI_JEONGSI,
            max_length=10,
            )
    
    def __str__(self):
        return f'{self.univ.name}|{self.sj}'


class JH(models.Model):
    class Meta:
        verbose_name = '전형'
        verbose_name_plural = '전형'

    sj = models.ForeignKey(
            verbose_name='수시/정시',
            to=SJ,
            related_name='jhs',
            on_delete=models.CASCADE,
            )
    name = models.CharField(
            verbose_name='전형명',
            max_length=30,
            )

    def __str__(self):
        return f'{self.sj.univ.name}|{self.sj.sj}|{self.name}'


class Major(models.Model):
    class Meta:
        verbose_name = '전형별 학과'
        verbose_name_plural = '전형별 학과'

    jh = models.ForeignKey(
            verbose_name='전형',
            to=JH,
            related_name='majors',
            on_delete=models.CASCADE,
            )
    name = models.CharField(
            verbose_name='학과명',
            max_length=50,
            )

    def __str__(self):
        return f'{self.jh.sj.univ.name}|{self.jh.sj.sj}|{self.jh.name}|{self.name}'


class Schedule(models.Model):
    class Meta:
        verbose_name = '학과별 일정'
        verbose_name_plural = '학과별 일정'

    major = models.ForeignKey(
            verbose_name='전형별 학과',
            to=Major,
            related_name='schedules',
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
        return f'{self.major.jh.sj.univ.name}|{self.major.jh.sj.sj}|{self.major.jh.name}|{self.major.name}|{self.description}'


class Device(models.Model):
    class Meta:
        verbose_name = '기기 정보'
        verbose_name_plural = '기기 정보'

    unique_id = models.CharField(
            verbose_name='기기 ID',
            max_length=50,
            unique=True,
            )
    majors = models.ManyToManyField(
            verbose_name='즐찾 학과',
            to=Major,
            related_name='devices',
            )

    def __str__(self):
        return self.unique_id
