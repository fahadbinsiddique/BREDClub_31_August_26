import sys
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

import setup_project
from .models import About, Mission, OrganizationInformation, SiteSettings, SocialLink, Vision


class PublicPagesTests(TestCase):
    def test_home_page_renders_without_site_settings(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)


class SeedContentTests(TestCase):
    def test_seed_content_creates_default_site_records(self):
        output = StringIO()

        call_command('seed_site_content', stdout=output)

        self.assertTrue(SiteSettings.objects.exists())
        self.assertTrue(About.objects.exists())
        self.assertTrue(OrganizationInformation.objects.exists())
        self.assertTrue(Mission.objects.exists())
        self.assertTrue(Vision.objects.exists())
        self.assertTrue(SocialLink.objects.exists())

    @patch.object(sys.modules['setup_project'], 'run_command')
    def test_setup_project_runs_required_commands(self, mock_run_command):
        setup_project.run_command = mock_run_command

        setup_project.main()

        self.assertEqual(mock_run_command.call_count, 5)
        self.assertIn(sys.executable, mock_run_command.call_args_list[0].args[0])
        self.assertIn('manage.py migrate', mock_run_command.call_args_list[0].args[0])
        self.assertIn('manage.py create_admin', mock_run_command.call_args_list[1].args[0])
        self.assertIn('manage.py seed_site_content', mock_run_command.call_args_list[2].args[0])
        self.assertIn('manage.py seed_sample_content', mock_run_command.call_args_list[3].args[0])
        self.assertIn('manage.py seed_gallery_content', mock_run_command.call_args_list[4].args[0])
