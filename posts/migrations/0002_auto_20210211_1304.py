# Generated by Django 3.1.6 on 2021-02-11 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply_comment',
            field=models.ManyToManyField(blank=True, null=True, related_name='_comment_reply_comment_+', to='posts.Comment'),
        ),
    ]
