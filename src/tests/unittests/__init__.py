import unittest


if __name__ == '__main__':
    # running every test in directory
    loader = unittest.TestLoader()
    tests = loader.discover('.')
    testRunner = unittest.TextTestRunner()
    testRunner.run(tests)
