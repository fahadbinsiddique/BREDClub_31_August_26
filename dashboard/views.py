from functools import wraps

from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST

from basic_app.forms import DASHBOARD_MODEL_FORMS, SiteSettingsForm
from basic_app.models import (
    About,
    Activity,
    Blog,
    BoardMember,
    Category,
    ContactMessage,
    ContactStatus,
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


DASHBOARD_MODULES = {
    "notices": {
        "title": "Notices",
        "model": Notice,
        "description": "Publish announcements and PDF notices.",
        "search": ("title", "summary", "content"),
    },
    "blogs": {
        "title": "Blogs",
        "model": Blog,
        "description": "Manage articles, categories, SEO, and rich text content.",
        "search": ("title", "excerpt", "content", "author", "category__name"),
    },
    "events": {
        "title": "Events",
        "model": Event,
        "description": "Create upcoming and past event listings.",
        "search": ("title", "description", "location"),
    },
    "trainings": {
        "title": "Trainings",
        "model": Training,
        "description": "Manage skill development training programs.",
        "search": ("title", "short_description", "description", "duration"),
    },
    "gallery-albums": {
        "title": "Gallery Albums",
        "model": Gallery,
        "description": "Group gallery images into albums.",
        "search": ("title", "description"),
    },
    "gallery-images": {
        "title": "Gallery Images",
        "model": GalleryImage,
        "description": "Upload and caption gallery photos.",
        "search": ("title", "caption", "gallery__title"),
    },
    "activities": {
        "title": "Activities",
        "model": Activity,
        "description": "Manage public activity areas and highlights.",
        "search": ("title", "short_description", "description", "highlights"),
    },
    "volunteers": {
        "title": "Volunteers",
        "model": Volunteer,
        "description": "Review and update volunteer applications.",
        "search": ("name", "email", "phone", "message"),
    },
    "contact-messages": {
        "title": "Contact Messages",
        "model": ContactMessage,
        "description": "Read and resolve contact form submissions.",
        "search": ("name", "email", "phone", "subject", "message"),
    },
    "board-members": {
        "title": "Board Members",
        "model": BoardMember,
        "description": "Manage leadership profiles for the board.",
        "search": ("name", "designation", "biography", "email", "phone"),
    },
    "executive-committee": {
        "title": "Executive Committee",
        "model": ExecutiveCommittee,
        "description": "Manage executive committee member profiles.",
        "search": ("name", "designation", "biography", "email", "phone"),
    },
    "categories": {
        "title": "Categories",
        "model": Category,
        "description": "Organize blog content by category.",
        "search": ("name", "description"),
    },
    "site-settings": {
        "title": "Site Settings",
        "model": SiteSettings,
        "description": "Control global organization, contact, and SEO settings.",
        "search": ("site_name", "tagline", "email_primary", "phone_primary", "address"),
    },
    "sliders": {
        "title": "Sliders",
        "model": Slider,
        "description": "Manage homepage hero slider content.",
        "search": ("title", "subtitle", "description"),
    },
    "about": {
        "title": "About",
        "model": About,
        "description": "Maintain the public about section.",
        "search": ("title", "subtitle", "description", "feature_list"),
    },
    "missions": {
        "title": "Missions",
        "model": Mission,
        "description": "Manage mission statements.",
        "search": ("title", "description"),
    },
    "visions": {
        "title": "Visions",
        "model": Vision,
        "description": "Manage vision statements.",
        "search": ("title", "description"),
    },
    "organization-information": {
        "title": "Organization Information",
        "model": OrganizationInformation,
        "description": "Update homepage counters and organization metrics.",
        "search": ("title",),
    },
    "social-links": {
        "title": "Social Links",
        "model": SocialLink,
        "description": "Manage footer and topbar social links.",
        "search": ("platform", "url"),
    },
}


def is_dashboard_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def dashboard_required(view_func):
    @wraps(view_func)
    @login_required(login_url="dashboard:login")
    def wrapped(request, *args, **kwargs):
        if not is_dashboard_user(request.user):
            messages.error(request, "Your account does not have dashboard access.")
            return redirect("home:index")
        return view_func(request, *args, **kwargs)

    return wrapped


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        if is_dashboard_user(request.user):
            return redirect("dashboard:overview")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not is_dashboard_user(user):
            messages.error(self.request, "Only staff and superuser accounts can access the dashboard.")
            return self.form_invalid(form)
        messages.success(self.request, "Welcome back to the dashboard.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_redirect_url() or reverse("dashboard:overview")


@login_required(login_url="dashboard:login")
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("dashboard:login")


@dashboard_required
def password_change(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully.")
            return redirect("dashboard:overview")
        messages.error(request, "Please correct the password form errors.")
    return render(request, "dashboard/password_change.html", {"form": form})


def get_module_config(module):
    config = DASHBOARD_MODULES.get(module)
    if not config:
        raise Http404("Dashboard module not found.")
    form_class = DASHBOARD_MODEL_FORMS.get(module)
    if not form_class:
        raise Http404("Dashboard form not found.")
    return {**config, "form_class": form_class, "slug": module}


def apply_dashboard_search(queryset, query, fields):
    if not query:
        return queryset
    search_query = Q()
    for field_name in fields:
        search_query |= Q(**{f"{field_name}__icontains": query})
    return queryset.filter(search_query)


def object_summary(obj):
    for field_name in ("summary", "excerpt", "short_description", "description", "message", "biography", "content"):
        value = getattr(obj, field_name, "")
        if value:
            return " ".join(str(value).split())[:140]
    return obj._meta.verbose_name.title()


def module_rows(queryset):
    rows = []
    for obj in queryset:
        rows.append(
            {
                "object": obj,
                "title": str(obj),
                "summary": object_summary(obj),
                "status": getattr(obj, "status", ""),
                "updated_at": getattr(obj, "updated_at", None),
            }
        )
    return rows


def module_cards():
    cards = []
    for slug, config in DASHBOARD_MODULES.items():
        cards.append(
            {
                "slug": slug,
                "title": config["title"],
                "description": config["description"],
                "count": config["model"].objects.count(),
            }
        )
    return cards


def detail_fields(obj):
    fields = []
    for field in obj._meta.fields:
        if field.name == "id":
            continue
        value = getattr(obj, field.name)
        display_method = getattr(obj, f"get_{field.name}_display", None)
        if display_method:
            value = display_method()
        is_file = hasattr(value, "url") if value else False
        fields.append(
            {
                "label": field.verbose_name.title(),
                "value": value,
                "is_file": is_file,
            }
        )
    return fields


@dashboard_required
def overview(request):
    stats = [
        ("Total Notices", Notice.objects.count()),
        ("Total Blogs", Blog.objects.count()),
        ("Total Events", Event.objects.count()),
        ("Total Trainings", Training.objects.count()),
        ("Total Gallery Images", GalleryImage.objects.count()),
        ("Total Activities", Activity.objects.count()),
        ("Total Volunteers", Volunteer.objects.count()),
        ("Total Contact Messages", ContactMessage.objects.count()),
        ("Total Board Members", BoardMember.objects.count()),
        ("Total Executive Members", ExecutiveCommittee.objects.count()),
    ]
    recent_activity = []
    for model, label in (
        (Notice, "Notice"),
        (Blog, "Blog"),
        (Event, "Event"),
        (Volunteer, "Volunteer"),
        (ContactMessage, "Contact Message"),
    ):
        for item in model.objects.order_by("-updated_at")[:3]:
            recent_activity.append(
                {
                    "label": label,
                    "title": str(item),
                    "updated_at": getattr(item, "updated_at", None),
                }
            )
    recent_activity = sorted(
        recent_activity,
        key=lambda item: item["updated_at"],
        reverse=True,
    )[:8]
    return render(request, "dashboard/overview.html", {"stats": stats, "recent_activity": recent_activity})


@dashboard_required
def content(request):
    return render(request, "dashboard/content.html", {"modules": module_cards()})


@dashboard_required
def module_list(request, module):
    config = get_module_config(module)
    query = request.GET.get("q", "").strip()
    queryset = apply_dashboard_search(
        config["model"].objects.all(),
        query,
        config["search"],
    )
    page_obj = Paginator(queryset, 12).get_page(request.GET.get("page"))
    context = {
        "module": config,
        "rows": module_rows(page_obj),
        "page_obj": page_obj,
        "query": query,
    }
    return render(request, "dashboard/module_list.html", context)


@dashboard_required
def module_detail(request, module, pk):
    config = get_module_config(module)
    obj = get_object_or_404(config["model"], pk=pk)
    return render(
        request,
        "dashboard/module_detail.html",
        {
            "module": config,
            "object": obj,
            "fields": detail_fields(obj),
        },
    )


@dashboard_required
def module_create(request, module):
    config = get_module_config(module)
    form = config["form_class"](request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"{config['title']} item created successfully.")
            return redirect("dashboard:module_detail", module=module, pk=obj.pk)
        messages.error(request, "Please correct the highlighted fields.")
    return render(
        request,
        "dashboard/module_form.html",
        {"module": config, "form": form, "mode": "Create"},
    )


@dashboard_required
def module_update(request, module, pk):
    config = get_module_config(module)
    obj = get_object_or_404(config["model"], pk=pk)
    form = config["form_class"](request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"{config['title']} item updated successfully.")
            return redirect("dashboard:module_detail", module=module, pk=obj.pk)
        messages.error(request, "Please correct the highlighted fields.")
    return render(
        request,
        "dashboard/module_form.html",
        {"module": config, "form": form, "object": obj, "mode": "Edit"},
    )


@dashboard_required
def module_delete(request, module, pk):
    config = get_module_config(module)
    obj = get_object_or_404(config["model"], pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"{config['title']} item deleted successfully.")
        return redirect("dashboard:module_list", module=module)
    return render(
        request,
        "dashboard/module_confirm_delete.html",
        {"module": config, "object": obj},
    )


@dashboard_required
def messages_inbox(request):
    selected_pk = request.GET.get("selected")
    message_list = ContactMessage.objects.order_by("ordering", "-created_at")
    selected_message = None
    if selected_pk:
        selected_message = get_object_or_404(ContactMessage, pk=selected_pk)
    elif message_list.exists():
        selected_message = message_list.first()

    if request.method == "POST" and selected_message:
        selected_message.status = ContactStatus.CLOSED
        selected_message.save(update_fields=["status", "updated_at"])
        messages.success(request, "Message marked as resolved.")
        return redirect(f"{reverse('dashboard:messages')}?selected={selected_message.pk}")

    return render(
        request,
        "dashboard/messages.html",
        {
            "message_list": message_list,
            "selected_message": selected_message,
        },
    )


@dashboard_required
def settings(request):
    instance = SiteSettings.objects.order_by("ordering", "-updated_at").first()
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings saved successfully.")
            return redirect("dashboard:settings")
        messages.error(request, "Please correct the site settings form.")
    return render(
        request,
        "dashboard/settings.html",
        {
            "form": form,
            "modules": [
                DASHBOARD_MODULES["organization-information"],
                DASHBOARD_MODULES["social-links"],
                DASHBOARD_MODULES["sliders"],
                DASHBOARD_MODULES["about"],
                DASHBOARD_MODULES["missions"],
                DASHBOARD_MODULES["visions"],
            ],
        },
    )
