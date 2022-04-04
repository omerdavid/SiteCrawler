from Dal.Models.siteModel import SiteModel
from Dal.Repositories.repositoryBase import RepositoryBase
from typing import List


class SitesRepository(RepositoryBase):

    def add(self, site: SiteModel):
        try:
            con = self.create_conection()
            con.execute(
                f'Insert INTO sites VALUES ({site.Name},{site.Url})')
            return
        except Exception as e:
            self.logger.error(e)
        finally:
            con.close()

    def get(self) -> List[SiteModel]:
        try:
            con = self.create_conection()
            sitesTable = con.execute('Select _sites.* from Sites as _sites')
            return self.__mapTupleListToSiteModelList(sitesTable.fetchall())
        except Exception as e:
            self.logger.error(e)
        finally:
            con.close()

    def __mapTupleListToSiteModelList(self, tupleList):
        try:
            siteModelList = []
            for site in tupleList:
                siteModelList.append(
                    self.__mapTupleToSiteModel(site))
            return siteModelList
        except Exception as e:
            self.logger.error(e)

    def __mapTupleToSiteModel(self, site_tuple):
        try:
            if site_tuple is not None:
                site_model = SiteModel()
                site_model.Id = site_tuple[0]
                site_model.Url = site_tuple[1]
                site_model.Name = site_tuple[2]
                return site_model
        except Exception as e:
            self.logger.error(e)
