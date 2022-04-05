

from BL.Models.Handlers.SiteCrawlerHandler import SiteCrawlerHandler
from BL.Services.CrawlSitesServiceBase import CrawlSitesServiceBase
import time
from Dal.Repositories.sitesRepository import SitesRepository
from SharedResourses.logService import LogService


class CrawlSiteService(CrawlSitesServiceBase):

    def __init__(self) -> None:
        try:
            super().__init__()
            self.__sitesRepo = SitesRepository()
            self.logger = LogService()
        except Exception as e:
            self.logger.error(e)

    def __getSitesList(self):
        try:
            return self.__sitesRepo.get()
        except Exception as e:
            self.logger.error(e)

    def CrawlSites(self):
        try:
            self.__sites = self.__getSitesList()

            while True:
                time.sleep(2)
                for site in self.__sites:
                    crawlerHandler = SiteCrawlerHandler(
                        site)
                    print(f'Start scan :{site.Url}')
                    self.logger.info(f'Start scan :{site.Url}')
                    crawlerHandler.CrawlSite()
                    print(f'Finish scan :{site.Url}')
                    self.logger.info(f'Finish scan :{site.Url}')
        except Exception as e:
            self.logger.error(e)
