import unittest

from julian.poller.services.nytpoller import NytPoller

class PollerTest( unittest.TestCase ):

  def setUp(self):
    pass

  def test_init(self):
    p = NytPoller()
