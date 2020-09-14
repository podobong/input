from django.db import models


SUSI_JEONGSI = (('수시', '수시'), ('정시', '정시'))


class Univ(models.Model):
    class Meta:
        verbose_name = '대학'
        verbose_name_plural = '대학'
        ordering = ['name']

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

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name


class SJ(models.Model):
    class Meta:
        verbose_name = '수시/정시'
        verbose_name_plural = '수시/정시'
        ordering = ['univ', 'sj']

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

    def __repr__(self):
        return f'{self.univ.name}|{self.sj}'

    def __lt__(self, other):
        if self.univ != other.univ:
            return self.univ < other.univ
        return self.sj < other.sj


class JH(models.Model):
    class Meta:
        verbose_name = '전형'
        verbose_name_plural = '전형'
        ordering = ['sj', 'name']

    sj = models.ForeignKey(
            verbose_name='수시/정시',
            to=SJ,
            related_name='jhs',
            on_delete=models.CASCADE,
    )
    name = models.CharField(
            verbose_name='전형명',
            max_length=255,
    )

    def __str__(self):
        return f'{self.sj.univ.name}|{self.sj.sj}|{self.name}'

    def __repr__(self):
        return f'{self.sj.univ.name}|{self.sj.sj}|{self.name}'

    def __lt__(self, other):
        if self.sj != other.sj:
            if self.sj.univ != other.sj.univ:
                return self.sj.univ < other.sj.univ
            return self.sj < other.sj
        return self.name < other.name


class Major(models.Model):
    class Meta:
        verbose_name = '전형별 학과'
        verbose_name_plural = '전형별 학과'
        ordering = ['jh', 'name']

    jh = models.ForeignKey(
            verbose_name='전형',
            to=JH,
            related_name='majors',
            on_delete=models.CASCADE,
    )
    name = models.CharField(
            verbose_name='학과명',
            max_length=255,
    )

    def __str__(self):
        return f'{self.jh.sj.univ.name}|{self.jh.sj.sj}|{self.jh.name}|{self.name}'

    def __repr__(self):
        return f'{self.jh.sj.univ.name}|{self.jh.sj.sj}|{self.jh.name}|{self.name}'

    def __lt__(self, other):
        if self.jh != other.jh:
            if self.jh.sj != other.jh.sj:
                if self.jh.sj.univ != other.jh.sj.univ:
                    return self.jh.sj.univ < other.jh.sj.univ
                return self.jh.sj < other.jh.sj
            return self.jh.name < other.jh.name
        return self.name < other.name


class Schedule(models.Model):
    class Meta:
        verbose_name = '학과별 일정'
        verbose_name_plural = '학과별 일정'
        ordering = ['start_date']

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
    is_offline = models.BooleanField(
            verbose_name='대면 시험 여부',
            default=False,
    )

    def __str__(self):
        return f'{self.major.jh.sj.univ.name}|{self.major.jh.sj.sj}|{self.major.jh.name}|{self.major.name}|{self.description}'

    def __repr__(self):
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
    token = models.CharField(
            verbose_name='기기 token',
            max_length=256,
    )

    def __str__(self):
        return self.unique_id

    def __repr__(self):
        return self.unique_id
