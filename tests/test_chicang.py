from unittest import TestCase
from dce.spiders.chicang import ChicangSpider
import os

class ChicangTest(TestCase):
    def setUp(self):
        self.target = ChicangSpider()

    def test_chicang_extract_data_from_file(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        data_file_path = os.path.join(dir, 'pages/20160622_pp1609_.txt')
        
        items = list(self.target.extract_data_from_file(data_file_path))
        
        print items