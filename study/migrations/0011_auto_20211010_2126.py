# Generated by Django 3.2.5 on 2021-10-10 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0010_auto_20211008_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='english',
            field=models.IntegerField(blank=True, null=True, verbose_name='英語'),
        ),
        migrations.AlterField(
            model_name='test',
            name='japanese',
            field=models.IntegerField(blank=True, null=True, verbose_name='国語'),
        ),
        migrations.AlterField(
            model_name='test',
            name='math',
            field=models.IntegerField(blank=True, null=True, verbose_name='数学'),
        ),
        migrations.AlterField(
            model_name='test',
            name='science',
            field=models.IntegerField(blank=True, null=True, verbose_name='理科'),
        ),
        migrations.AlterField(
            model_name='test',
            name='social_studies',
            field=models.IntegerField(blank=True, null=True, verbose_name='社会'),
        ),
    ]