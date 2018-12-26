import re


class Utils:
    def is_staging(url):
        result = re.match('^.*?-sta\..*$', url)
        #result = re.match('^.*.io$', url)
        #result = re.match('^.*$', url)
        if result:
            return True
        return False

    def url_matches_site_name(name, url):
        if name in url:
            return True
        return False
