
class FakeClient(object):

    def assert_called(self, method, url, body=None, pos=-1):
        """
        Assert than an API method was just called.
        """
        expected = (method, url)
        called = self.client.callstack[pos][0:2]

        assert self.client.callstack, \
            "Expected %s %s but no calls were made." % expected

        assert expected == called, \
            'Expected %s %s; got %s %s' % (expected + called)

        if body is not None:
            if self.client.callstack[pos][2] != body:
                raise AssertionError('%r != %r' %
                                     (self.client.callstack[pos][2], body))

    def assert_called_anytime(self, method, url, body=None, partial_body=None):
        """
        Assert than an API method was called anytime in the test.
        """
        expected = (method, url)

        assert self.client.callstack, ("Expected %s %s but no calls "
                                       "were made." % expected)

        found = False
        for entry in self.client.callstack:
            if expected == entry[0:2]:
                found = True
                break

        assert found, 'Expected %s %s; got %s' % (
            expected + (self.client.callstack, ))

        if body is not None:
            try:
                assert entry[2] == body
            except AssertionError:
                print(entry[2])
                print("!=")
                print(body)
                raise

        if partial_body is not None:
            try:
                assert self._dict_match(partial_body, entry[2])
            except AssertionError:
                print(entry[2])
                print("does not contain")
                print(partial_body)
                raise

    def clear_callstack(self):
        self.client.callstack = []

    def authenticate(self):
        pass
