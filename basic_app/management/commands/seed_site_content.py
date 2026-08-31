from django.core.management.base import BaseCommand

from basic_app.models import (
    About,
    Mission,
    OrganizationInformation,
    PublishStatus,
    SiteSettings,
    SocialLink,
    Vision,
)


class Command(BaseCommand):
    help = 'Create starter content for the public site when no content has been added yet.'

    def handle(self, *args, **options):
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name='BREDClub',
                tagline='Empowerment Through Development',
                footer_about='The Business Research & Entrepreneurs Development Club Bangladesh is committed to community development through education, training, and empowerment.',
                address='Dhanmondi, Dhaka-1205, Bangladesh',
                phone_primary='+880 1700-000000',
                email_primary='info@bredclub.org',
                copyright_text='Copyright 2026 BREDClub. All rights reserved.',
                developed_by='Designed & Developed by PyBROTHERS Team',
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )

        if not About.objects.exists():
            About.objects.create(
                title='About BREDClub',
                subtitle='Who We Are',
                description='BREDClub is a youth-focused development organization working to empower communities through education, entrepreneurship, research, and training.',
                years_of_excellence=10,
                feature_list='Community development\nSkill-based training\nYouth empowerment',
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )

        if not OrganizationInformation.objects.exists():
            OrganizationInformation.objects.create(
                title='Organization Information',
                active_members=500,
                completed_projects=120,
                training_workshops=40,
                events_organized=75,
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )

        if not Mission.objects.exists():
            Mission.objects.create(
                title='Our Mission',
                description='To empower individuals and communities through knowledge, skills, and inclusive development initiatives.',
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )

        if not Vision.objects.exists():
            Vision.objects.create(
                title='Our Vision',
                description='To build a more educated, skilled, and self-reliant society through collaborative development efforts.',
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )

        if not SocialLink.objects.exists():
            SocialLink.objects.create(
                platform='Facebook',
                url='https://facebook.com',
                icon_name='facebook',
                status=PublishStatus.PUBLISHED,
                ordering=0,
            )
            SocialLink.objects.create(
                platform='LinkedIn',
                url='https://linkedin.com',
                icon_name='linkedin',
                status=PublishStatus.PUBLISHED,
                ordering=1,
            )

        self.stdout.write(self.style.SUCCESS('Starter site content created successfully.'))
