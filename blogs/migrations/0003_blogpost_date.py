from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_blogpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='date',
            field=models.DateTimeField(default=timezone.now),
            preserve_default=False,
        ),
    ]
