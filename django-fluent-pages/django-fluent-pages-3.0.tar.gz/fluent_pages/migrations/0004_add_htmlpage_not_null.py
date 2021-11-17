# Generated by Django 1.11.4 on 2017-08-05 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("fluent_pages", "0003_set_htmlpage_defaults")]

    operations = [
        migrations.AlterField(
            model_name="htmlpagetranslation",
            name="meta_description",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Typically, about 160 characters will be shown in search engines",
                max_length=255,
                verbose_name="description",
            ),
        ),
        migrations.AlterField(
            model_name="htmlpagetranslation",
            name="meta_image",
            field=models.ImageField(
                blank=True,
                default="",
                help_text="This allows social media sites to pick a default image.",
                upload_to="",
                verbose_name="example image",
            ),
        ),
        migrations.AlterField(
            model_name="htmlpagetranslation",
            name="meta_keywords",
            field=models.CharField(
                blank=True, default="", max_length=255, verbose_name="keywords"
            ),
        ),
        migrations.AlterField(
            model_name="htmlpagetranslation",
            name="meta_title",
            field=models.CharField(
                blank=True,
                default="",
                help_text="When this field is not filled in, the menu title text will be used.",
                max_length=255,
                verbose_name="page title",
            ),
        ),
    ]
