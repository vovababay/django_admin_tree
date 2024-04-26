from django.test import TestCase


class TestCaseOne(TestCase):
    def test_one(self):
        self.assertEqual(1, 1)