from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def clean(self):
        if not self.name or self.name.strip() == '':
            raise ValidationError('Category name cannot be null or empty')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"