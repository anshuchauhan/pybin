import HTMLParser

class Validator(object):

    """
        Parses input, a dictionary, and applies rules to each and reports errors

        Rules:
            Each value must at least have three characters
            Non code fields to have unsafe elements & tokens removed
            (more to add here)
    """

    def __init__(self, input):
        self.input = input
        self.valid = True
        self.issues = []
        tmp = {}

        for k, v in self.input.items():

            if k != "code":
                tmp[k] = self.strip_tags(v)
            else:
                tmp[k] = v
                if k != "type" and len(v) < 3:
                    self.valid = False
                    self.issues.append("%s needs to have at least 3 characters" % k)

        self.input = tmp



    def is_valid(self):
        return self.valid

    def get_issues(self):
        return self.issues

    def get_vars(self):
        return self.input

    def get_var(self, key):
        try:
            return self.input[key]
        except KeyError:
            return None

    def strip_tags(self, raw):
        s = StripTags()
        s.feed(raw)
        return s.getSafeString()

class StripTags(HTMLParser.HTMLParser):

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.reset()
        self.stripped = []

    def handle_data(self, data):
        self.stripped.append(data)

    def getSafeString(self):
        return "".join(self.stripped)
