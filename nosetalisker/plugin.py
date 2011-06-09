from datetime import datetime

import cProfile
import logging
import os

import tempfile

from nose.plugins import Plugin

log = logging.getLogger('nose.plugins.talisker')

class Talisker(Plugin):
    """
    Outputs a profile for each test into a profile directory
    using Python's standard profile modules.
    """
    name = 'talisker'

    def options(self, parser, env):
        Plugin.options(self, parser, env)
        parser.add_option('--prof-path', action='store', dest='prof_path',
                          help="The directory to write profile files too.")

    def begin(self, *args, **kw):
        pass

    def configure(self, options, conf):
        path = options.prof_path
        if not path:
            self.prof_path = tempfile.mkdtemp()
        else:
            assert os.path.exists(path)
            assert os.path.isdir(path)
            self.prof_path = path
        print "configure", path

    def prepareTestCase(self, test):
        print "running test", test
        def run_and_profile(result, test=test):
            prof = cProfile.Profile()
            start = datetime.now()
            prof.runcall(test.test, result)
            elap = datetime.now() - start
            elapms = elap.seconds * 1000.0 + elap.microseconds / 1000.0
            dest = '%s.%06dms.%s.prof' % (test.test, elapms, datetime.now().isoformat())
            dest = os.path.join(self.prof_path, dest)
            prof.dump_stats(dest)
        return run_and_profile

    def beforeTest(self, test):
        print "beforeTest", test

    def afterTest(self, test):
        print "afterTest", test
