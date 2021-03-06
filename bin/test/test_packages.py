from test_service import Service, Stanza
from test_path import PathTestCase
import os
import r_packages
from unittest import TestCase


class PackagesTestCase(PathTestCase):
    def test_update_library(self):
        service = Service([
            Stanza('package://boot', {}),
        ])
        r_packages.update_library(service)
        installed_packages = os.listdir(r_packages.get_library_path())
        self.assertEqual(len(installed_packages), 1)
        self.assertEqual(installed_packages[0], 'boot')
        self.assertEqual(r_packages.get_package_state('boot'), r_packages.metadata_package_installed)
        r_packages.update_library(service)
        installed_packages = os.listdir(r_packages.get_library_path())
        self.assertEqual(len(installed_packages), 1)
        self.assertEqual(installed_packages[0], 'boot')
        self.assertEqual(r_packages.get_package_state('boot'), r_packages.metadata_package_installed)
        r_packages.add(service, 'forecast')
        self.assertEqual(r_packages.get_package_state('forecast'), r_packages.metadata_package_not_installed)
        r_packages.update_library(service)
        installed_packages = os.listdir(r_packages.get_library_path())
        self.assertTrue('boot' in installed_packages)
        self.assertTrue('forecast' in installed_packages)
        self.assertEqual(r_packages.get_package_state('boot'), r_packages.metadata_package_installed)
        self.assertEqual(r_packages.get_package_state('forecast'), r_packages.metadata_package_installed)
        r_packages.remove(service, 'boot')
        self.assertEqual(r_packages.get_package_state('boot'), r_packages.metadata_package_installed)
        r_packages.update_library(service)
        installed_packages = os.listdir(r_packages.get_library_path())
        self.assertFalse('boot' in installed_packages)
        self.assertTrue('timeDate' in installed_packages)
        self.assertTrue('forecast' in installed_packages)
        self.assertEqual(r_packages.get_package_state('boot'), r_packages.metadata_package_not_installed)
        self.assertEqual(r_packages.get_package_state('timeDate'), r_packages.metadata_package_installed)
        self.assertEqual(r_packages.get_package_state('forecast'), r_packages.metadata_package_installed)


class PackageArchiveTests(TestCase):
    def test_extract_package_name(self):
        sample_package_archives_dir = os.path.join(os.path.dirname(__file__), 'sample_package_archives')
        for archive_file_name in os.listdir(sample_package_archives_dir):
            if not archive_file_name.startswith('.'):
                with open(os.path.join(sample_package_archives_dir, archive_file_name)) as f:
                    name = r_packages.get_package_name_from_archive_file(archive_file_name, f)
                    self.assertTrue(archive_file_name.startswith(name),'Extracted %s from %s' % (name, archive_file_name))