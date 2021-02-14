# Generated by Django 3.1.6 on 2021-02-11 07:59

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
            name='Hobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='hobby_image/')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='profile/default_profile.jpg', upload_to='profile/')),
                ('cover_image', models.ImageField(default='cover/default_cover.jpg', upload_to='cover/')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPrivacy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.CharField(choices=[('friend', 'Friends'), ('public', 'Public (Any one)'), ('me', 'Only me')], default='public', max_length=50)),
                ('date_of_birth', models.CharField(choices=[('friend', 'Friends'), ('public', 'Public (Any one)'), ('me', 'Only me')], default='public', max_length=50)),
                ('phone_number', models.CharField(choices=[('friend', 'Friends'), ('public', 'Public (Any one)'), ('me', 'Only me')], default='public', max_length=50)),
                ('friends', models.CharField(choices=[('friend', 'Friends'), ('public', 'Public (Any one)'), ('me', 'Only me')], default='public', max_length=50)),
                ('search', models.CharField(choices=[('friend', 'Friends'), ('public', 'Public (Any one)'), ('me', 'Only me')], default='public', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_privacy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserHobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hobby', to='profiles.hobby')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_hobby', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_complete', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_education', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]