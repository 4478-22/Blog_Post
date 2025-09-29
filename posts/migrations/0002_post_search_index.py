from django.db import migrations
from django.contrib.postgres.operations import CreateExtension
from django.contrib.postgres.indexes import GinIndex

def add_search_index(apps, schema_editor):
    # No data op needed; we’ll just ensure extension exists via separate operation if needed.
    pass

class Migration(migrations.Migration):
    dependencies = [("posts", "0001_initial")]

    operations = [
        # Ensure pg_trgm and unaccent are available (optional but helpful)
        CreateExtension("pg_trgm"),
        CreateExtension("unaccent"),
        migrations.AddIndex(
            model_name="post",
            index=GinIndex(
                name="post_content_gin",
                fields=["content"],
                opclasses=["gin_trgm_ops"],  # speeds LIKE/ILIKE and similarity
            ),
        ),
    ]
