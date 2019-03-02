# Generated by Django 2.1.7 on 2019-02-24 03:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('github', models.CharField(max_length=150)),
                ('displayName', models.CharField(max_length=150)),
                ('bio', models.TextField()),
                ('host', models.URLField()),
                ('friends', models.ManyToManyField(blank=True, null=True, related_name='reverse_friends', to='socialapp.Author')),
                ('localuser', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('contentType', models.CharField(max_length=64)),
                ('published', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialapp.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('source', models.URLField()),
                ('origin', models.URLField()),
                ('description', models.CharField(max_length=280)),
                ('contentType', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('published', models.DateTimeField()),
                ('visibility', models.CharField(max_length=64)),
                ('unlisted', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='socialapp.Author')),
            ],
        ),
        migrations.CreateModel(
            name='PostTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialapp.PostTags'),
        ),
        migrations.AddField(
            model_name='post',
            name='visibleTo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visibleTo', to='socialapp.Author'),
        ),
    ]