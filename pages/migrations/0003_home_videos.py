# Generated by Django 2.2.7 on 2019-12-19 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_video_details_channel_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='home_videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('discription', models.CharField(max_length=500, null=True)),
                ('video_id', models.CharField(max_length=500, null=True)),
                ('channel_name', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
