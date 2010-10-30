from toast.tests import *

class TestCommandController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='command', action='index'))
        # Test response...
