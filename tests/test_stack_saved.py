import sys
import os
# Add the parent directory to path so Python can find the mode_0 package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import greenlet
from . import TestCase


class Test(TestCase):

    def test_stack_saved(self):
        main = greenlet.getcurrent()
        self.assertEqual(main._stack_saved, 0)

        def func():
            main.switch(main._stack_saved)

        g = greenlet.greenlet(func)
        x = g.switch()
        self.assertGreater(x, 0)
        self.assertGreater(g._stack_saved, 0)
        g.switch()
        self.assertEqual(g._stack_saved, 0)
