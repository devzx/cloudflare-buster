class SiteError(Exception):
    def __init__(self, message):
        self.message = message


class UnableToListSiteError(SiteError):
    pass


class UnableToPurgeCacheError(SiteError):
    pass


class NonStagingSiteError(SiteError):
    pass
