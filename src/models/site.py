import CloudFlare

from src.common.utils import Utils
from src.common import errors as SiteError


class SiteModel:
    def __init__(self, name, _id):
        self.name = name
        self.id = _id
        self.environment = None

    def __repr__(self):
        return f'<Site {self.name}>'

    @classmethod
    def get_from_cloudflare(cls, _id=None):
        """
        Returns a list of SiteModel objects for all zones found in Cloudflare.
        If an id is passed returns a single instance of that zone
        """
        try:
            cf = CloudFlare.CloudFlare()
            zones = cf.zones.get(_id, params={'per_page': 100})
        except:
            raise SiteError.UnableToListSiteError(
                'Error occurred when trying to retrieve the sites')

        return cls(zones['name'], zones['id']) if _id else \
            [cls(zone['name'], zone['id']) for zone in zones]

    @staticmethod
    def get_sites():
        """
        Returns a list of SiteModel objects with the environment set
        """
        sites = SiteModel.get_from_cloudflare()
        for site in sites:
            if Utils.is_staging(site.name):
                site.environment = 'staging'
            else:
                site.environment = 'production'

        return sites

    @staticmethod
    def get_one_site(_id):
        """
        Takes a zone id and returns an instance of SiteModel
        """
        site = SiteModel.get_from_cloudflare(_id)

        return site

    def purge_all_cache(self):
        """
        Purges all files within a sites Cloudflare cache
        """
        if not Utils.is_staging(self.name):
            raise SiteError.NonStagingSiteError(
                f'Unable to preform action for {self.name}')
        try:
            cf = CloudFlare.CloudFlare()
            cf.zones.purge_cache.delete(self.id,
                                        data={'purge_everything': True})
        except:
            raise SiteError.UnableToPurgeCacheError(
                'Error occured when trying to purge the cache')

    def purge_items_in_cache(self, urls):
        """
        Purges indiviual files within a sites Cloudflare cache
        """
        valid_urls = [url for url in urls
                      if Utils.url_matches_site_name(self.name, url)]
        if valid_urls:
            try:
                cf = CloudFlare.CloudFlare()
                cf.zones.purge_cache.delete(self.id, data={'files': valid_urls})
            except:
                raise SiteError.UnableToPurgeCacheError(
                    'Error occured while trying to purge the cache')

        return valid_urls

    @staticmethod
    def purge_all_staging_cache():
        """
        Purges the entire cache for all staging sites
        """
        staging_sites = [site for site in SiteModel.get_sites()
                         if Utils.is_staging(site.name)]
        for site in staging_sites:
            print(f'Purging cache for {site}')
            site.purge_all_cache()
