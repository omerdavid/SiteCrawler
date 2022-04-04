

from BL.Services.CrawlSiteService import CrawlSiteService
from SharedResourses.logService import LogService

if __name__ == "__main__":
    print('Start siteCrawl app...')
    try:
        crawl = CrawlSiteService()
        crawl.CrawlSites()
        
    except Exception as e:
        logger = LogService()
        logger.error(e)
    finally:
        print('Stop siteCrawl app...')