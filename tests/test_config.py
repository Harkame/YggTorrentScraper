import unittest

import yggtorrentscraper.helpers


class ConfigTest(unittest.TestCase):
    def test_get_config(self):
        config = helpers.get_config(os.path.join('.', 'tests', 'test_config', 'test_config.yml'))
        self.assertEqual(config['destination_path'], './mymangas/')
        self.assertEqual(config['list_research'][0]['name'], 'The.Walking.Dead.S09')
