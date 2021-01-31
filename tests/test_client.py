import unittest
from src.api.client import Client


class TestImporterClient(unittest.TestCase):

    def setUp(self):
        self.client = Client()
