from django.contrib import admin
from .models import Course, Review


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ("title", "slug", "is_active")
    list_display = ("title", "created_date", "updated_date", "is_active")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("course", "name", "email", "rating", "created_date")
    list_filter = ("course", "created_date", "rating")
