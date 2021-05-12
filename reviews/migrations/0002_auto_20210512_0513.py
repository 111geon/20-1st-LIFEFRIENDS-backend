# Generated by Django 3.2.2 on 2021-05-12 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_image_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'reviewimages',
            },
        ),
        migrations.AlterField(
            model_name='review',
            name='review_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.reviewimage'),
        ),
        migrations.DeleteModel(
            name='Review_Image',
        ),
    ]
