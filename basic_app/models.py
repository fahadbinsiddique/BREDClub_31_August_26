from pathlib import Path

from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "gif"]
DOCUMENT_EXTENSIONS = ["pdf"]


def unique_slugify(instance, value, slug_field_name="slug"):
    base_slug = slugify(value)[:50] or "item"
    slug = base_slug
    index = 2
    model_class = instance.__class__

    while True:
        lookup = {slug_field_name: slug}
        queryset = model_class._default_manager.filter(**lookup)
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)
        if not queryset.exists():
            return slug
        suffix = f"-{index}"
        slug = f"{base_slug[:50 - len(suffix)]}{suffix}"
        index += 1


class PublishStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class BaseContentModel(models.Model):
    status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED,
    )
    ordering = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("ordering", "-created_at")


class SEOMixin(models.Model):
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(
        upload_to="seo/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )

    class Meta:
        abstract = True

    def get_meta_title(self):
        return self.meta_title or str(self)

    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        for field_name in ("summary", "short_description", "excerpt", "description", "content"):
            value = getattr(self, field_name, "")
            if value:
                return " ".join(str(value).split())[:155]
        return ""


class Category(BaseContentModel, SEOMixin):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class BoardMember(BaseContentModel):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    photo = models.ImageField(
        upload_to="board-members/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Board Member"
        verbose_name_plural = "Board Members"

    def __str__(self):
        return f"{self.name} - {self.designation}"


class ExecutiveCommittee(BaseContentModel):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    photo = models.ImageField(
        upload_to="executive-committee/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Executive Committee Member"
        verbose_name_plural = "Executive Committee Members"

    def __str__(self):
        return f"{self.name} - {self.designation}"


class Activity(BaseContentModel, SEOMixin):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(
        upload_to="activities/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    highlights = models.TextField(
        blank=True,
        help_text="Enter one highlight per line.",
    )
    icon_name = models.CharField(max_length=80, blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title

    @property
    def highlight_list(self):
        return [item.strip() for item in self.highlights.splitlines() if item.strip()]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class TrainingStatus(models.TextChoices):
    UPCOMING = "upcoming", "Upcoming"
    ONGOING = "ongoing", "Ongoing"
    COMPLETED = "completed", "Completed"


class Training(BaseContentModel, SEOMixin):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(
        upload_to="training/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    duration = models.CharField(max_length=80, blank=True)
    seats = models.PositiveIntegerField(default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    training_status = models.CharField(
        max_length=20,
        choices=TrainingStatus.choices,
        default=TrainingStatus.UPCOMING,
    )
    application_link = models.URLField(blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Training"
        verbose_name_plural = "Trainings"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class Event(BaseContentModel, SEOMixin):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=180)
    poster = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    registration_link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta(BaseContentModel.Meta):
        ordering = ("date", "time", "ordering")
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.date >= timezone.localdate()

    def get_absolute_url(self):
        return reverse("home:event_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class Blog(BaseContentModel, SEOMixin):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="blogs",
    )
    author = models.CharField(max_length=120, blank=True)
    featured_image = models.ImageField(
        upload_to="blogs/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)

    class Meta(BaseContentModel.Meta):
        ordering = ("ordering", "-published_at")
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("home:blog_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class Gallery(BaseContentModel, SEOMixin):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    cover_image = models.ImageField(
        upload_to="gallery/albums/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    description = models.TextField(blank=True)
    event_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Gallery Album"
        verbose_name_plural = "Gallery Albums"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class GalleryImage(BaseContentModel):
    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.CASCADE,
        related_name="images",
    )
    title = models.CharField(max_length=180)
    image = models.ImageField(
        upload_to="gallery/images/",
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    caption = models.TextField(blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.title


class Notice(BaseContentModel, SEOMixin):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    published_date = models.DateField(default=timezone.localdate)
    pdf_file = models.FileField(
        upload_to="notices/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=DOCUMENT_EXTENSIONS)],
    )
    is_pinned = models.BooleanField(default=False)

    class Meta(BaseContentModel.Meta):
        ordering = ("-is_pinned", "ordering", "-published_date")
        verbose_name = "Notice"
        verbose_name_plural = "Notices"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("home:notice_detail", kwargs={"slug": self.slug})

    @property
    def filename(self):
        if not self.pdf_file:
            return ""
        return Path(self.pdf_file.name).name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class VolunteerStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class Volunteer(models.Model):
    AREA_CHOICES = [
        ("education", "Education Support"),
        ("youth", "Youth Development"),
        ("health", "Healthcare"),
        ("women", "Women Empowerment"),
        ("environment", "Environmental Protection"),
        ("disaster", "Disaster Management"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    area = models.CharField(max_length=30, choices=AREA_CHOICES)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=VolunteerStatus.choices,
        default=VolunteerStatus.PENDING,
    )
    ordering = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("ordering", "-created_at")
        verbose_name = "Volunteer"
        verbose_name_plural = "Volunteers"

    def __str__(self):
        return f"{self.name} - {self.get_area_display()}"


class ContactStatus(models.TextChoices):
    NEW = "new", "New"
    READ = "read", "Read"
    REPLIED = "replied", "Replied"
    CLOSED = "closed", "Closed"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ContactStatus.choices,
        default=ContactStatus.NEW,
    )
    ordering = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("ordering", "-created_at")
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.subject} - {self.name}"


class SiteSettings(BaseContentModel, SEOMixin):
    site_name = models.CharField(max_length=120, default="BREDClub")
    tagline = models.CharField(
        max_length=180,
        default="Empowerment Through Development",
    )
    logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    footer_about = models.TextField(blank=True)
    address = models.TextField(blank=True)
    phone_primary = models.CharField(max_length=30, blank=True)
    phone_secondary = models.CharField(max_length=30, blank=True)
    email_primary = models.EmailField(blank=True)
    email_secondary = models.EmailField(blank=True)
    office_hours = models.CharField(max_length=180, blank=True)
    google_map_embed = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=180, blank=True)
    developed_by = models.CharField(max_length=120, blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    @classmethod
    def load(cls):
        return cls.objects.filter(status=PublishStatus.PUBLISHED).order_by("ordering", "-updated_at").first()


class Slider(BaseContentModel):
    title = models.CharField(max_length=180)
    subtitle = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="sliders/",
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    primary_button_text = models.CharField(max_length=80, blank=True)
    primary_button_url = models.CharField(max_length=255, blank=True)
    secondary_button_text = models.CharField(max_length=80, blank=True)
    secondary_button_url = models.CharField(max_length=255, blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"

    def __str__(self):
        return self.title


class About(BaseContentModel, SEOMixin):
    title = models.CharField(max_length=220)
    subtitle = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )
    years_of_excellence = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    feature_list = models.TextField(
        blank=True,
        help_text="Enter one feature per line.",
    )

    class Meta(BaseContentModel.Meta):
        verbose_name = "About"
        verbose_name_plural = "About"

    def __str__(self):
        return self.title

    @property
    def features(self):
        return [item.strip() for item in self.feature_list.splitlines() if item.strip()]

    @classmethod
    def load(cls):
        return cls.objects.filter(status=PublishStatus.PUBLISHED).order_by("ordering", "-updated_at").first()


class Mission(BaseContentModel):
    title = models.CharField(max_length=160, default="Our Mission")
    description = models.TextField()
    icon_name = models.CharField(max_length=80, blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Mission"
        verbose_name_plural = "Missions"

    def __str__(self):
        return self.title


class Vision(BaseContentModel):
    title = models.CharField(max_length=160, default="Our Vision")
    description = models.TextField()
    icon_name = models.CharField(max_length=80, blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Vision"
        verbose_name_plural = "Visions"

    def __str__(self):
        return self.title


class OrganizationInformation(BaseContentModel):
    title = models.CharField(max_length=160, default="Organization Information")
    active_members = models.PositiveIntegerField(default=0)
    completed_projects = models.PositiveIntegerField(default=0)
    training_workshops = models.PositiveIntegerField(default=0)
    events_organized = models.PositiveIntegerField(default=0)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Organization Information"
        verbose_name_plural = "Organization Information"

    def __str__(self):
        return self.title

    @classmethod
    def load(cls):
        return cls.objects.filter(status=PublishStatus.PUBLISHED).order_by("ordering", "-updated_at").first()


class SocialLink(BaseContentModel):
    platform = models.CharField(max_length=80)
    url = models.URLField()
    icon_name = models.CharField(max_length=80, blank=True)

    class Meta(BaseContentModel.Meta):
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.platform
