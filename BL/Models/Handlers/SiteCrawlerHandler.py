
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
            siteContent = requests.get(self.__site.Url)
            tree = html.fromstring(siteContent.content)
            pastesLinks = self.__extractPastesLinksFromHtml(tree)
            pastes = self.__buildPastesBySpecificPageLink(pastesLinks)
            newPastes = self.__filterNewPastes(pastes)
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
            normalizeParamList = paramRepo.get()
            for htmlAnchorTag in pastesLinks:
                pasteSpecificPageTree = self.__getPasteSpecificPage(
                    htmlAnchorTag)
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
