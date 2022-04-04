
from Dal.Models.pasteModel import PasteModel
from Dal.Repositories.repositoryBase import RepositoryBase


class PastesRepository(RepositoryBase):

    def add(self, paste):
        try:
            con = self.create_conection()
            query = "Insert INTO Pastes VALUES (NULL,?,?,?,?)"
            con.execute(query, (paste.Author, paste.Content,
                        paste.Date, paste.Title))
            con.commit()
        except Exception as e:
            self.logger.error(e)
        finally:
            con.close()

    def get(self, author):
        try:
            con = self.create_conection()
            query = "Select ps.Id,ps.Author,ps.Date,ps.Content,ps.Title from "
            f"Pastes ps where author='{author}'"
            authorPastes = con.execute(query).fetchall()
            return authorPastes
        except Exception as e:
            self.logger.error(e)
        finally:
            con.close()

    def isPasteExist(self, paste: PasteModel):
        try:
            con = self.create_conection()
            query = f"Select COUNT(ps.Id) from Pastes ps where author='{paste.Author}' and Date='{paste.Date}' and Title='{paste.Title}' "
            pasteCount = con.execute(query).fetchone()
            return pasteCount[0] > 0
        except Exception as e:
            self.logger.error(e)
        finally:
            con.close()
