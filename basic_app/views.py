from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

from .forms import ContactMessageForm, VolunteerForm
from .models import (
    About,
    Activity,
    Blog,
    BoardMember,
    Category,
    Event,
    ExecutiveCommittee,
    Gallery,
    GalleryImage,
    Mission,
    Notice,
    OrganizationInformation,
    PublishStatus,
    Slider,
    Training,
    Vision,
)


DEFAULT_META_DESCRIPTION = (
    "BREDClub - The Business Research and Entrepreneurs Development Club Bangladesh."
)


def published(model):
    return model.objects.filter(status=PublishStatus.PUBLISHED)


def paginate(request, queryset, per_page):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def apply_search(queryset, query, fields):
    if not query:
        return queryset
    search_query = Q()
    for field_name in fields:
        search_query |= Q(**{f"{field_name}__icontains": query})
    return queryset.filter(search_query)


def base_meta(title, description=DEFAULT_META_DESCRIPTION, keywords=""):
    return {
        "meta_title": title,
        "meta_description": description,
        "meta_keywords": keywords,
    }


def index(request):
    today = timezone.localdate()
    context = {
        **base_meta("BREDClub - Building Resources for Empowerment and Development"),
        "sliders": published(Slider),
        "about": About.load(),
        "organization": OrganizationInformation.load(),
        "featured_activities": published(Activity).filter(is_featured=True)[:6],
        "latest_activities": published(Activity)[:6],
        "featured_trainings": published(Training)[:3],
        "upcoming_events": published(Event).filter(date__gte=today).order_by("date", "time")[:3],
        "latest_blogs": published(Blog).select_related("category")[:3],
        "gallery_images": published(GalleryImage).select_related("gallery")[:6],
        "latest_notices": published(Notice)[:3],
        "missions": published(Mission)[:3],
        "visions": published(Vision)[:3],
    }
    return render(request, "home/index.html", context)


def about(request):
    about_content = About.load()
    description = about_content.get_meta_description() if about_content else DEFAULT_META_DESCRIPTION
    context = {
        **base_meta("About Us - BREDClub", description),
        "about": about_content,
        "missions": published(Mission),
        "visions": published(Vision),
        "organization": OrganizationInformation.load(),
    }
    return render(request, "home/about.html", context)


def board_members(request):
    query = request.GET.get("q", "").strip()
    queryset = apply_search(
        published(BoardMember),
        query,
        ["name", "designation", "biography"],
    )
    context = {
        **base_meta("Board of Members - BREDClub"),
        "members": queryset,
        "query": query,
    }
    return render(request, "home/board_members.html", context)


def executive_committee(request):
    query = request.GET.get("q", "").strip()
    queryset = apply_search(
        published(ExecutiveCommittee),
        query,
        ["name", "designation", "biography"],
    )
    context = {
        **base_meta("Executive Committee - BREDClub"),
        "members": queryset,
        "query": query,
    }
    return render(request, "home/executive_committee.html", context)


def activities(request):
    context = {
        **base_meta("Our Activities - BREDClub"),
        "activities": published(Activity),
    }
    return render(request, "home/activities.html", context)


def training(request):
    context = {
        **base_meta("Training Programs - BREDClub"),
        "trainings": published(Training),
    }
    return render(request, "home/training.html", context)


def events(request):
    query = request.GET.get("q", "").strip()
    queryset = apply_search(
        published(Event).order_by("date", "time"),
        query,
        ["title", "description", "location"],
    )
    context = {
        **base_meta("Events - BREDClub"),
        "events": paginate(request, queryset, 6),
        "query": query,
    }
    return render(request, "home/events.html", context)


def event_detail(request, slug):
    event = get_object_or_404(published(Event), slug=slug)
    related_events = (
        published(Event)
        .exclude(pk=event.pk)
        .filter(date__gte=timezone.localdate())
        .order_by("date", "time")[:3]
    )
    context = {
        **base_meta(event.get_meta_title(), event.get_meta_description(), event.keywords),
        "event": event,
        "related_events": related_events,
    }
    return render(request, "home/event_detail.html", context)


def blog(request):
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    queryset = published(Blog).select_related("category")

    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    queryset = apply_search(queryset, query, ["title", "excerpt", "content", "author", "category__name"])

    context = {
        **base_meta("Blog - BREDClub"),
        "blogs": paginate(request, queryset, 6),
        "categories": published(Category),
        "recent_posts": published(Blog)[:5],
        "query": query,
        "category_slug": category_slug,
    }
    return render(request, "home/blog.html", context)


def blog_detail(request, slug):
    post = get_object_or_404(published(Blog).select_related("category"), slug=slug)
    related_posts = published(Blog).exclude(pk=post.pk)
    if post.category_id:
        related_posts = related_posts.filter(category=post.category)
    context = {
        **base_meta(post.get_meta_title(), post.get_meta_description(), post.keywords),
        "post": post,
        "recent_posts": published(Blog).exclude(pk=post.pk)[:5],
        "related_posts": related_posts[:3],
    }
    return render(request, "home/blog_detail.html", context)


def gallery(request):
    albums = published(Gallery).prefetch_related("images")
    images = published(GalleryImage).select_related("gallery")
    context = {
        **base_meta("Gallery - BREDClub"),
        "albums": albums,
        "images": paginate(request, images, 9),
    }
    return render(request, "home/gallery.html", context)


def notice(request):
    query = request.GET.get("q", "").strip()
    queryset = apply_search(
        published(Notice),
        query,
        ["title", "summary", "content"],
    )
    context = {
        **base_meta("Notice Board - BREDClub"),
        "notices": paginate(request, queryset, 7),
        "query": query,
    }
    return render(request, "home/notice.html", context)


def notice_detail(request, slug):
    notice_obj = get_object_or_404(published(Notice), slug=slug)
    context = {
        **base_meta(notice_obj.get_meta_title(), notice_obj.get_meta_description(), notice_obj.keywords),
        "notice": notice_obj,
        "recent_notices": published(Notice).exclude(pk=notice_obj.pk)[:5],
    }
    return render(request, "home/notice_detail.html", context)


def volunteer(request):
    form = VolunteerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Your volunteer application has been submitted successfully.")
            return redirect("home:volunteer")
        messages.error(request, "Please correct the highlighted fields and try again.")

    context = {
        **base_meta("Volunteer - BREDClub"),
        "form": form,
    }
    return render(request, "home/volunteer.html", context)


def contact(request):
    form = ContactMessageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect("home:contact")
        messages.error(request, "Please correct the highlighted fields and try again.")

    context = {
        **base_meta("Contact Us - BREDClub"),
        "form": form,
    }
    return render(request, "home/contact.html", context)


def sitemap_xml(request):
    url_names = [
        "home:index",
        "home:about",
        "home:board_members",
        "home:executive_committee",
        "home:activities",
        "home:training",
        "home:events",
        "home:blog",
        "home:gallery",
        "home:notice",
        "home:volunteer",
        "home:contact",
    ]
    locations = [request.build_absolute_uri(reverse(name)) for name in url_names]
    locations.extend(request.build_absolute_uri(post.get_absolute_url()) for post in published(Blog))
    locations.extend(request.build_absolute_uri(event.get_absolute_url()) for event in published(Event))
    locations.extend(request.build_absolute_uri(item.get_absolute_url()) for item in published(Notice))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for location in locations:
        lines.append(f"  <url><loc>{escape(location)}</loc></url>")
    lines.append("</urlset>")
    return HttpResponse("\n".join(lines), content_type="application/xml")


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("home:sitemap"))
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /dashboard/",
            f"Sitemap: {sitemap_url}",
        ]
    )
    return HttpResponse(content, content_type="text/plain")


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)


def ext(request):    
    
    # Top-level executive loop chain
    board = BoardMember.objects.filter(designation__icontains="Board").first()
    founder = BoardMember.objects.filter(designation__icontains="Founder").exclude(designation__icontains="Co").first()
    co_founder = BoardMember.objects.filter(designation__icontains="Co-Founder").first()

    # Base query for department heads (Directors) who report directly to Executive level
    directors = BoardMember.objects.filter(parent=co_founder)

    context = {
        'board': board,
        'founder': founder,
        'co_founder': co_founder,
        'directors': directors,
    }
    return render(request, 'home/org_chart.html', context)

