# Generated by Django 2.1.7 on 2019-03-30 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0005_auto_20190328_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='basicToken',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='post',
            name='contentType',
            field=models.CharField(choices=[('image/jpeg;base64', 'JPEG'), ('text/plain', 'Plain'), ('application/base64', 'File'), ('text/markdown', 'Markdown'), ('image/png;base64', 'PNG')], default='text/markdown', max_length=64),
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('FOAF', 'Private to Friends of Friends'), ('PRIVATE', 'Private To Me (And Selected People)'), ('FRIENDS', 'Private to Friends'), ('SERVERONLY', 'Public To This Host'), ('PUBLIC', 'Public')], default='PUBLIC', max_length=64),
        ),
    ]