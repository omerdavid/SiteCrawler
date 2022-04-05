
from typing import List
import requests
from lxml import html
from BL.Builders.pastesBuilder import PasteBuilder

from Dal.Models.pasteModel import PasteModel
from Dal.Models.siteModel import SiteModel
from Dal.Repositories.normalizeParamRepository import NormalizeParamRepository
from Dal.Repositories.pastesRepository import PastesRepository
from SharedResourses.logService import LogService


class SiteCrawlerHandler:

    def __init__(self, site: SiteModel) -> None:
        self.__site = site
        self.logger = LogService()

    def CrawlSite(self):
        try:
            # sending ajax request to get site html
            siteContent = requests.get(self.__site.Url)

            # parsing the html to an object document for data to be extracted
            tree = html.fromstring(siteContent.content)

            # extracting the pastes anchor tags from main/home page
            # in order to get a single paste data from the paste specific page
            pastesLinks = self.__extractPastesLinksFromHtml(tree)

            pastes = self.__buildPastesBySpecificPageLink(pastesLinks)

            # filter already existing pastes
            newPastes = self.__filterNewPastes(pastes)

            # adding new pastes to db
            self.__addNewpastes(newPastes)
        except Exception as e:
            self.logger.error(e)

    def __extractPastesLinksFromHtml(self, tree):
        try:
            pastesLinks = tree.xpath('//ul[@class="sidebar__menu"]/li/a')
            return pastesLinks
        except Exception as e:
            self.logger.error(e)

    def __buildPastesBySpecificPageLink(self, pastesLinks):
        try:
            pastes = []
            pasteBuilder = PasteBuilder()
            paramRepo = NormalizeParamRepository()

            # getting a ready list from db to normalize param
            # which considered as "same value"
            normalizeParamList = paramRepo.get()
            for htmlAnchorTag in pastesLinks:
                pasteSpecificPageTree = self.__getPasteSpecificPage(
                    htmlAnchorTag)

                # extract and parse paste data from html using dedicated
                # paste builder which returns a ready PasteModel
                paste = pasteBuilder.Build(
                    pasteSpecificPageTree, normalizeParamList)
                pastes.append(paste)
            return pastes
        except Exception as e:
            self.logger.error(e)

    def __getPasteSpecificPage(self, htmlAnchorTag):
        try:
            href = htmlAnchorTag.get('href')
            pasteSpecificPage = requests.get(self.__site.Url+href)
            pasteSpecificPageTree = html.fromstring(pasteSpecificPage.content)
            return pasteSpecificPageTree
        except Exception as e:
            self.logger.error(e)

    def __filterNewPastes(self, pastes: List[PasteModel]):
        try:
            pasteRepo = PastesRepository()
            newPastes = []
            for paste in pastes:
                isPasteExist = pasteRepo.isPasteExist(paste)
                if isPasteExist is False:
                    newPastes.append(paste)

            return newPastes
        except Exception as e:
            self.logger.error(e)

    def __addNewpastes(self,  newPastes: List[PasteModel]):
        try:
            pasteRepo = PastesRepository()
            for newPaste in newPastes:
                pasteRepo.add(newPaste)
        except Exception as e:
            self.logger.error(e)
