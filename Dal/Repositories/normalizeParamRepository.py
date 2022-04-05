

from Dal.Models.normalizeParamModel import NormalizeParamModel
from Dal.Repositories.repositoryBase import RepositoryBase


class NormalizeParamRepository(RepositoryBase):

    # adding new Entity to db
    def add(self, param):
        try:
            con = self.create_conection()
            con.execute(
                "Insert INTO NormalizeParam VALUES "
                f"('{param.Id}','{param.Name}','{param.type}')")
            return con.lastrowid
        except Exception as e:
            self.logger.error(e)
        finally:
            con.close()

    # get all Entity records
    def get(self):
        try:
            con = self.create_conection()
            query = 'Select np.Id,np.Name,np.ParamType from NormalizeParam np'
            normalizeParamList = con.execute(query).fetchall()
            return self.__mapTupleListToNormalizeParamModelList(
                normalizeParamList)
        except Exception as e:
            self.logger.error(e)
        finally:
            con.close()

    def __mapTupleListToNormalizeParamModelList(self, tupleList):
        try:
            normalizeParamModelList = []
            for norParam in tupleList:
                normalizeParamModelList.append(
                    self.__mapTupleToNormalizeParamModel(norParam))
            return normalizeParamModelList
        except Exception as e:
            self.logger.error(e)

    def __mapTupleToNormalizeParamModel(self, tuple):
        try:
            newModel = NormalizeParamModel()
            newModel.Id = tuple[0]
            newModel.Name = tuple[1]
            newModel.ParamType = tuple[2]
            return newModel
        except Exception as e:
            self.logger.error(e)
