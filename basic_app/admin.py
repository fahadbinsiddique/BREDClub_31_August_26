from django.contrib import admin
from django.utils.html import format_html

from .models import (
    About,
    Activity,
    Blog,
    BoardMember,
    Category,
    ContactMessage,
    Event,
    ExecutiveCommittee,
    Gallery,
    GalleryImage,
    Mission,
    Notice,
    OrganizationInformation,
    SiteSettings,
    Slider,
    SocialLink,
    Training,
    Vision,
    Volunteer,
)


def image_preview(obj):
    image_field_names = (
        "photo",
        "image",
        "featured_image",
        "cover_image",
        "poster",
        "logo",
        "favicon",
        "og_image",
    )
    for field_name in image_field_names:
        image = getattr(obj, field_name, None)
        if image:
            return format_html(
                '<img src="{}" style="height:56px;width:72px;object-fit:cover;border-radius:6px;" />',
                image.url,
            )
    return "-"


image_preview.short_description = "Preview"


class BaseAdmin(admin.ModelAdmin):
    list_filter = ("status", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("ordering", "-created_at")


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ("name", "slug", "status", "ordering", "updated_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BoardMember)
class BoardMemberAdmin(BaseAdmin):
    list_display = ("name", "designation", "status", "ordering", image_preview, "updated_at")
    search_fields = ("name", "designation", "biography", "email", "phone")


@admin.register(ExecutiveCommittee)
class ExecutiveCommitteeAdmin(BoardMemberAdmin):
    pass


@admin.register(Activity)
class ActivityAdmin(BaseAdmin):
    list_display = ("title", "is_featured", "status", "ordering", image_preview, "updated_at")
    search_fields = ("title", "short_description", "description", "highlights")
    list_filter = ("is_featured", "status", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Training)
class TrainingAdmin(BaseAdmin):
    list_display = ("title", "training_status", "duration", "seats", "status", "ordering", image_preview)
    search_fields = ("title", "short_description", "description", "duration")
    list_filter = ("training_status", "status", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Event)
class EventAdmin(BaseAdmin):
    list_display = ("title", "date", "time", "location", "is_featured", "status", image_preview)
    search_fields = ("title", "description", "location")
    list_filter = ("is_featured", "date", "status", "created_at", "updated_at")
    ordering = ("date", "time", "ordering")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Blog)
class BlogAdmin(BaseAdmin):
    list_display = ("title", "category", "author", "published_at", "is_featured", "status", image_preview)
    search_fields = ("title", "excerpt", "content", "author")
    list_filter = ("category", "is_featured", "status", "published_at", "created_at")
    ordering = ("ordering", "-published_at")
    prepopulated_fields = {"slug": ("title",)}


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ("title", "image", "caption", "status", "ordering")


@admin.register(Gallery)
class GalleryAdmin(BaseAdmin):
    list_display = ("title", "event_date", "is_featured", "status", "ordering", image_preview)
    search_fields = ("title", "description")
    list_filter = ("is_featured", "event_date", "status", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (GalleryImageInline,)


@admin.register(GalleryImage)
class GalleryImageAdmin(BaseAdmin):
    list_display = ("title", "gallery", "status", "ordering", image_preview, "updated_at")
    search_fields = ("title", "caption", "gallery__title")
    list_filter = ("gallery", "status", "created_at", "updated_at")


@admin.register(Notice)
class NoticeAdmin(BaseAdmin):
    list_display = ("title", "published_date", "is_pinned", "status", "ordering", "pdf_link", "updated_at")
    search_fields = ("title", "summary", "content")
    list_filter = ("is_pinned", "published_date", "status", "created_at", "updated_at")
    ordering = ("-is_pinned", "ordering", "-published_date")
    prepopulated_fields = {"slug": ("title",)}

    @admin.display(description="PDF")
    def pdf_link(self, obj):
        if not obj.pdf_file:
            return "-"
        return format_html('<a href="{}" target="_blank">Download</a>', obj.pdf_file.url)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "area", "status", "created_at")
    search_fields = ("name", "email", "phone", "message")
    list_filter = ("area", "status", "created_at", "updated_at")
    ordering = ("ordering", "-created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "phone", "status", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    list_filter = ("status", "created_at", "updated_at")
    ordering = ("ordering", "-created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseAdmin):
    list_display = ("site_name", "tagline", "email_primary", "phone_primary", "status", image_preview)
    search_fields = ("site_name", "tagline", "email_primary", "phone_primary", "address")


@admin.register(Slider)
class SliderAdmin(BaseAdmin):
    list_display = ("title", "subtitle", "status", "ordering", image_preview, "updated_at")
    search_fields = ("title", "subtitle", "description")


@admin.register(About)
class AboutAdmin(BaseAdmin):
    list_display = ("title", "subtitle", "years_of_excellence", "status", "ordering", image_preview)
    search_fields = ("title", "subtitle", "description", "feature_list")


@admin.register(Mission)
class MissionAdmin(BaseAdmin):
    list_display = ("title", "status", "ordering", "updated_at")
    search_fields = ("title", "description")


@admin.register(Vision)
class VisionAdmin(MissionAdmin):
    pass


@admin.register(OrganizationInformation)
class OrganizationInformationAdmin(BaseAdmin):
    list_display = (
        "title",
        "active_members",
        "completed_projects",
        "training_workshops",
        "events_organized",
        "status",
    )
    search_fields = ("title",)


@admin.register(SocialLink)
class SocialLinkAdmin(BaseAdmin):
    list_display = ("platform", "url", "status", "ordering", "updated_at")
    search_fields = ("platform", "url")
