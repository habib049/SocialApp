# Generated by Django 3.1.6 on 2021-02-11 07:55

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
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Post title')),
                ('sub_title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Subtitle')),
                ('content', models.TextField(blank=True, null=True)),
                ('click_num', models.IntegerField(default=0, verbose_name='Number of clicks')),
                ('like_num', models.IntegerField(default=0, verbose_name='Number of likes')),
                ('dislike_num', models.IntegerField(default=0, verbose_name='Number of dislikes')),
                ('comment_num', models.IntegerField(default=0, verbose_name='Number of comments')),
                ('add_time', models.DateTimeField(auto_now=True, verbose_name='Post add time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='post_images/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_image', to='posts.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('add_time', models.DateTimeField(auto_now=True, help_text='comment add time', verbose_name='comment add time')),
                ('comment_level', models.IntegerField(default=0)),
                ('tree_id', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='posts.post')),
                ('reply_comment', models.ManyToManyField(related_name='_comment_reply_comment_+', to='posts.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]