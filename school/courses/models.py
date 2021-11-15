from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify


class Base(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]
        abstract = True


class Course(Base):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # url = models.URLField(unique=True)

    class Meta:
        ordering = ["title"]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(Base):
    course = models.ForeignKey(Course, related_name="reviews", on_delete=CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    comment = models.TextField(blank=True, default="")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ["email", "course"]
        ordering = ["-created_date"]


    def __str__(self):
        return (
            f"{self.name} reviewed the course {self.course} with a rating of {self.rating}"
        )
