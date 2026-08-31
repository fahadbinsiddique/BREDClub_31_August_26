from .models import OrganizationInformation, PublishStatus, SiteSettings, SocialLink


def global_site_context(request):
    site_settings = SiteSettings.load() or SiteSettings()
    organization_info = OrganizationInformation.load() or OrganizationInformation()
    social_links = SocialLink.objects.filter(status=PublishStatus.PUBLISHED).order_by("ordering", "platform")

    return {
        "site_settings": site_settings,
        "organization_info": organization_info,
        "social_links": social_links,
        "canonical_url": request.build_absolute_uri(request.path),
    }
