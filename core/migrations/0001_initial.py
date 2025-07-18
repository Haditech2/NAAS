# Generated by Django 4.2.23 on 2025-07-08 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('role', models.CharField(blank=True, max_length=100)),
                ('content', models.TextField()),
                ('is_featured', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('content', models.TextField()),
                ('category', models.CharField(choices=[('general', 'General News'), ('events', 'Event Updates'), ('scholarship', 'Scholarships'), ('achievements', 'Student Achievements')], default='general', max_length=50)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_published', models.BooleanField(default=True)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='news_images/')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news_articles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'News',
                'ordering': ['-published_date'],
            },
        ),
        migrations.CreateModel(
            name='Executive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('president', 'President'), ('vice_president', 'Vice President'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('publicity', 'Publicity Secretary'), ('welfare', 'Welfare Officer'), ('other', 'Other')], max_length=50)),
                ('bio', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='executives/')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='executive_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
    ]
