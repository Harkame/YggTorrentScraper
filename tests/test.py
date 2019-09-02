import sys
import unittest

if __name__ == '__main__':
    iterations = 5

    for iteration in range(iterations):
        sucess = unittest.main(exit=False, argv=unitargs).result.wasSuccessful()

        if not sucess:
            sys.exit(1)
