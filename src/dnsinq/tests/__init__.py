import unittest


def make_suite():  # pragma: no cover
    test_suite = unittest.TestLoader().discover(
        'dnsinq.tests', pattern='test_*.py',
    )
    return test_suite
