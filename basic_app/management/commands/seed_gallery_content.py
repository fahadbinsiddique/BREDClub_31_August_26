from django.core.management.base import BaseCommand

from basic_app.models import Gallery, GalleryImage, PublishStatus


class Command(BaseCommand):
    help = 'Create sample gallery albums and images for the public gallery page.'

    def handle(self, *args, **options):
        if not Gallery.objects.exists():
            album = Gallery.objects.create(
                title='Community Outreach',
                slug='community-outreach',
                description='Photos from our community engagement activities.',
                is_featured=True,
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )
            GalleryImage.objects.create(
                gallery=album,
                title='Outreach Session',
                image='gallery/images/outreach-session.jpg',
                caption='A community session hosted by the club.',
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )
            GalleryImage.objects.create(
                gallery=album,
                title='Volunteer Team',
                image='gallery/images/volunteer-team.jpg',
                caption='Volunteers working together on a local program.',
                status=PublishStatus.PUBLISHED,
                ordering=1,
            )

        self.stdout.write(self.style.SUCCESS('Gallery sample content created successfully.'))
