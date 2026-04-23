from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    is_released = models.BooleanField(default=False)  # вышла серия или нет
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)
    rutube_url = models.URLField(null=True, blank=True)
    vk_url = models.URLField(null=True, blank=True)
    kion_url = models.URLField(null=True, blank=True)
    okko_url = models.URLField(null=True, blank=True)
    kinopoisk_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class HeroSuggestion(models.Model):
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()      # визионерство
    contacts = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.user_id} ({self.category})"

class PremiereSubscriber(models.Model):
    user_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PartnerRequest(models.Model):
    user_id = models.BigIntegerField()
    company_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)