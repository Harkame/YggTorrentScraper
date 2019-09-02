import unittest

import helpers


class TestArgument(unittest.TestCase):
    def test_short_option(self):
        arguments = helpers.get_arguments(['-v', '-c', './myconfig.yml', '-i', 'myidentifiant', '-p', 'mypassword'])

        self.assertEqual(arguments.verbose, 1)
        self.assertEqual(arguments.config_file, './myconfig.yml')
        self.assertEqual(arguments.identifiant, 'myidentifiant')
        self.assertEqual(arguments.password, 'mypassword')

    def test_long_option(self):
        arguments = helpers.get_arguments(['--verbose', '--config_file', './myconfig.yml', '--identifiant', 'myidentifiant', '--password', 'mypassword'])

        self.assertEqual(arguments.verbose, 1)
        self.assertEqual(arguments.config_file, './myconfig.yml')
        self.assertEqual(arguments.identifiant, 'myidentifiant')
        self.assertEqual(arguments.password, 'mypassword')

    def test_multiple_verbose(self):
        verbosity_argument = '-'

        for verbosity_level in range(1, 10):
            verbosity_argument += 'v'
            arguments = helpers.get_arguments([verbosity_argument])
            self.assertEqual(arguments.verbose, verbosity_level)
