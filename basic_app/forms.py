from django import forms

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


class StyledModelForm(forms.ModelForm):
    image_max_size = 5 * 1024 * 1024
    document_max_size = 10 * 1024 * 1024

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "dashboard-checkbox")
                continue
            widget.attrs.setdefault("class", "form-control")
            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("rows", 5)
            if isinstance(widget, forms.DateInput):
                widget.input_type = "date"
            if isinstance(widget, forms.TimeInput):
                widget.input_type = "time"

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if not hasattr(value, "size"):
                continue
            max_size = self.document_max_size if field_name.endswith("pdf_file") else self.image_max_size
            if value.size > max_size:
                size_mb = max_size // (1024 * 1024)
                self.add_error(field_name, f"File size must be {size_mb}MB or smaller.")
        return cleaned_data


class CategoryForm(StyledModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
            "description",
            "meta_title",
            "meta_description",
            "keywords",
            "og_image",
            "status",
            "ordering",
        ]


class BoardMemberForm(StyledModelForm):
    class Meta:
        model = BoardMember
        fields = [
            "name",
            "designation",
            "photo",
            "biography",
            "email",
            "phone",
            "facebook_url",
            "linkedin_url",
            "twitter_url",
            "status",
            "ordering",
        ]


class ExecutiveCommitteeForm(BoardMemberForm):
    class Meta(BoardMemberForm.Meta):
        model = ExecutiveCommittee


class ActivityForm(StyledModelForm):
    class Meta:
        model = Activity
        fields = [
            "title",
            "slug",
            "image",
            "short_description",
            "description",
            "highlights",
            "icon_name",
            "is_featured",
            "meta_title",
            "meta_description",
            "keywords",
            "og_image",
            "status",
            "ordering",
        ]


class TrainingForm(StyledModelForm):
    class Meta:
        model = Training
        fields = [
            "title",
            "slug",
            "image",
            "short_description",
            "description",
            "duration",
            "seats",
            "start_date",
            "end_date",
            "fee",
            "training_status",
            "application_link",
            "meta_title",
            "meta_description",
            "keywords",
            "og_image",
            "status",
            "ordering",
        ]


class EventForm(StyledModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "slug",
            "description",
            "date",
            "time",
            "location",
            "poster",
            "registration_link",
            "is_featured",
            "meta_title",
            "meta_description",
            "keywords",
            "og_image",
            "status",
            "ordering",
        ]


class BlogForm(StyledModelForm):
    class Meta:
        model = Blog
        fields = [
            "title",
            "slug",
            "category",
            "author",
            "featured_image",
            "excerpt",
            "content",
            "published_at",
            "is_featured",
            "meta_title",
            "meta_description",
            "keywords",
            "og_image",
            "status",
            "ordering",
        ]
        widgets = {
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class GalleryForm(StyledModelForm):
    class Meta:
        model = Gallery
        fields = [
            "title",
            "slug",
            "cover_image",
            "description",
            "event_date",
            "is_featured",
            "meta_title",
            "meta_description",
            "keywords",
            "og_image",
            "status",
            "ordering",
        ]


class GalleryImageForm(StyledModelForm):
    class Meta:
        model = GalleryImage
        fields = [
            "gallery",
            "title",
            "image",
            "caption",
            "status",
            "ordering",
        ]


class NoticeForm(StyledModelForm):
    class Meta:
        model = Notice
        fields = [
            "title",
            "slug",
            "summary",
            "content",
            "published_date",
            "pdf_file",
            "is_pinned",
            "meta_title",
            "meta_description",
            "keywords",
            "og_image",
            "status",
            "ordering",
        ]


class VolunteerForm(StyledModelForm):
    class Meta:
        model = Volunteer
        fields = [
            "name",
            "email",
            "phone",
            "area",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email address"}),
            "phone": forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
            "area": forms.Select(attrs={"placeholder": "Choose your area of interest"}),
            "message": forms.Textarea(attrs={"placeholder": "Tell us why you want to volunteer"}),
        }

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class VolunteerDashboardForm(StyledModelForm):
    class Meta:
        model = Volunteer
        fields = [
            "name",
            "email",
            "phone",
            "area",
            "message",
            "status",
            "ordering",
        ]


class ContactMessageForm(StyledModelForm):
    class Meta:
        model = ContactMessage
        fields = [
            "name",
            "email",
            "phone",
            "subject",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email address"}),
            "phone": forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
            "subject": forms.TextInput(attrs={"placeholder": "What is your message about?"}),
            "message": forms.Textarea(attrs={"placeholder": "Write your message here"}),
        }

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class ContactMessageDashboardForm(StyledModelForm):
    class Meta:
        model = ContactMessage
        fields = [
            "name",
            "email",
            "phone",
            "subject",
            "message",
            "status",
            "ordering",
        ]


class SiteSettingsForm(StyledModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            "site_name",
            "tagline",
            "logo",
            "favicon",
            "footer_about",
            "address",
            "phone_primary",
            "phone_secondary",
            "email_primary",
            "email_secondary",
            "office_hours",
            "google_map_embed",
            "copyright_text",
            "developed_by",
            "meta_title",
            "meta_description",
            "keywords",
            "og_image",
            "status",
            "ordering",
        ]


class SliderForm(StyledModelForm):
    class Meta:
        model = Slider
        fields = [
            "title",
            "subtitle",
            "description",
            "image",
            "primary_button_text",
            "primary_button_url",
            "secondary_button_text",
            "secondary_button_url",
            "status",
            "ordering",
        ]


class AboutForm(StyledModelForm):
    class Meta:
        model = About
        fields = [
            "title",
            "subtitle",
            "description",
            "image",
            "years_of_excellence",
            "feature_list",
            "meta_title",
            "meta_description",
            "keywords",
            "og_image",
            "status",
            "ordering",
        ]


class MissionForm(StyledModelForm):
    class Meta:
        model = Mission
        fields = [
            "title",
            "description",
            "icon_name",
            "status",
            "ordering",
        ]


class VisionForm(MissionForm):
    class Meta(MissionForm.Meta):
        model = Vision


class OrganizationInformationForm(StyledModelForm):
    class Meta:
        model = OrganizationInformation
        fields = [
            "title",
            "active_members",
            "completed_projects",
            "training_workshops",
            "events_organized",
            "status",
            "ordering",
        ]


class SocialLinkForm(StyledModelForm):
    class Meta:
        model = SocialLink
        fields = [
            "platform",
            "url",
            "icon_name",
            "status",
            "ordering",
        ]


DASHBOARD_MODEL_FORMS = {
    "categories": CategoryForm,
    "board-members": BoardMemberForm,
    "executive-committee": ExecutiveCommitteeForm,
    "activities": ActivityForm,
    "trainings": TrainingForm,
    "events": EventForm,
    "blogs": BlogForm,
    "gallery-albums": GalleryForm,
    "gallery-images": GalleryImageForm,
    "notices": NoticeForm,
    "volunteers": VolunteerDashboardForm,
    "contact-messages": ContactMessageDashboardForm,
    "site-settings": SiteSettingsForm,
    "sliders": SliderForm,
    "about": AboutForm,
    "missions": MissionForm,
    "visions": VisionForm,
    "organization-information": OrganizationInformationForm,
    "social-links": SocialLinkForm,
}
