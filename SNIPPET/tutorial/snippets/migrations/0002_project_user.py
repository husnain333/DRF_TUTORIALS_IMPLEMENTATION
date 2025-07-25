# Generated by Django 5.2.4 on 2025-07-25 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('url', models.URLField(blank=True)),
                ('UUID', models.UUIDField(editable=False, unique=True)),
                ('file_path', models.FilePathField(match='.*\\.txt$', path='/path/to/files', recursive=True)),
                ('ipadress', models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('float1', models.FloatField(default=0.0)),
                ('slarayDate', models.DateField(auto_now=True)),
                ('timestarted', models.TimeField(auto_now_add=True, null=True)),
                ('shift_duration', models.DurationField(default='00:00:00')),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
            ],
            options={
                'ordering': ['username'],
            },
        ),
    ]
