from django.core.management.base import BaseCommand
from django.utils import timezone

from basic_app.models import Blog, Category, Event, Notice, PublishStatus


class Command(BaseCommand):
    help = 'Create sample blog, event, and notice content for the public site.'

    def handle(self, *args, **options):
        if not Category.objects.exists():
            Category.objects.create(name='Development', slug='development', description='Development-related posts', status=PublishStatus.PUBLISHED, ordering=0)
            Category.objects.create(name='Training', slug='training', description='Training-related posts', status=PublishStatus.PUBLISHED, ordering=1)

        if not Blog.objects.exists():
            category = Category.objects.order_by('ordering').first()
            Blog.objects.create(
                title='Welcome to BREDClub',
                slug='welcome-to-bredclub',
                category=category,
                author='BREDClub Team',
                excerpt='A short introduction to our mission and the work we do for communities.',
                content='BREDClub focuses on building practical opportunities for youth and communities through training, research, entrepreneurship, and collaboration.',
                published_at=timezone.now(),
                is_featured=True,
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )
            Blog.objects.create(
                title='Upcoming Training Opportunities',
                slug='upcoming-training-opportunities',
                category=Category.objects.get(slug='training'),
                author='Program Team',
                excerpt='We are preparing new training sessions in leadership, entrepreneurship, and digital skills.',
                content='Our upcoming programs will help participants grow practically and build confidence in their chosen paths.',
                published_at=timezone.now(),
                status=PublishStatus.PUBLISHED,
                ordering=1,
            )

        if not Event.objects.exists():
            Event.objects.create(
                title='Community Outreach Program',
                slug='community-outreach-program',
                description='Join us for a weekend outreach event focused on mentorship and local support.',
                date=timezone.localdate(),
                time=timezone.now().time(),
                location='Dhaka',
                registration_link='https://example.com',
                is_featured=True,
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )

        if not Notice.objects.exists():
            Notice.objects.create(
                title='New Volunteer Registration Open',
                slug='new-volunteer-registration-open',
                summary='Volunteer registration is now open for the next community development cycle.',
                content='Interested individuals can sign up through the volunteer page and join upcoming efforts across the country.',
                published_date=timezone.localdate(),
                is_pinned=True,
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )

        self.stdout.write(self.style.SUCCESS('Sample public content created successfully.'))
