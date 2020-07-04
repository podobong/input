# Generated by Django 3.0.8 on 2020-07-04 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JH',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='전형명')),
                ('like', models.IntegerField(default=0, verbose_name='즐찾')),
            ],
            options={
                'verbose_name': '전형',
                'verbose_name_plural': '전형',
            },
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='학과명')),
                ('like', models.IntegerField(default=0, verbose_name='즐찾')),
                ('jh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='majors', to='univ.JH', verbose_name='전형')),
            ],
            options={
                'verbose_name': '전형별 학과',
                'verbose_name_plural': '전형별 학과',
            },
        ),
        migrations.CreateModel(
            name='Univ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='대학명')),
                ('logo', models.ImageField(blank=True, upload_to='', verbose_name='로고 이미지')),
                ('review_url', models.CharField(blank=True, max_length=100, verbose_name='리뷰 URL')),
                ('like', models.IntegerField(default=0, verbose_name='즐찾')),
            ],
            options={
                'verbose_name': '대학',
                'verbose_name_plural': '대학',
            },
        ),
        migrations.CreateModel(
            name='SJ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sj', models.CharField(choices=[('수시', '수시'), ('정시', '정시')], max_length=10, verbose_name='수시/정시')),
                ('univ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sjs', to='univ.Univ', verbose_name='대학')),
            ],
            options={
                'verbose_name': '수시/정시',
                'verbose_name_plural': '수시/정시',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='일정 설명')),
                ('start_date', models.DateTimeField(verbose_name='시작 시간')),
                ('end_date', models.DateTimeField(verbose_name='종료 시간')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='univ.Major', verbose_name='전형별 학과')),
            ],
            options={
                'verbose_name': '학과별 일정',
                'verbose_name_plural': '학과별 일정',
            },
        ),
        migrations.AddField(
            model_name='jh',
            name='sj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jhs', to='univ.SJ', verbose_name='수시/정시'),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=50, verbose_name='기기 ID')),
                ('majors', models.ManyToManyField(related_name='devices', to='univ.Major', verbose_name='즐찾 학과')),
            ],
            options={
                'verbose_name': '기기 정보',
                'verbose_name_plural': '기기 정보',
            },
        ),
    ]
