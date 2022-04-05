

import logging
from BL.Builders.builderBase import BuilderBase
from Dal.Models.pasteModel import PasteModel
from lxml import html
from datetime import datetime
import re


class PasteBuilder(BuilderBase):

    def Build(self, pasteSpecificPageTree, normalizeParamList):
        try:
            paste = PasteModel()
            authorName = self.__extractPasteAuthor(pasteSpecificPageTree)
            paste.Author = self.__normalizeName(
                normalizeParamList, authorName, 'Author')
            title = self.__extractPasteTitle(pasteSpecificPageTree)
            paste.Title = self.__normalizeName(
                normalizeParamList, title, 'Title')
            paste.Date = self.__extractPasteDate(pasteSpecificPageTree)
            paste.Content = self.__extractPasteContent(pasteSpecificPageTree)
            return paste
        except Exception as ex:
            logging.exception(ex)

    def __extractPasteTitle(self, pasteSpecificPageTree):
        try:
            pasteTitle = pasteSpecificPageTree.xpath(
                '//div[@class="info-top"]/h1/text()')
            return pasteTitle[0]
        except Exception as ex:
            logging.exception(ex)

    def __extractPasteAuthor(self, pasteSpecificPageTree):
        try:
            pasteAuthor = pasteSpecificPageTree.xpath(
                '//div[@class="username"]/a/text()')
            return pasteAuthor[0]
        except Exception as ex:
            logging.exception(ex)

    def __normalizeName(self, normalizeParamList, name, paramType):
        try:
            # filter normalizeParamList by paramType
            # ex:Author or Title from list

            paramTypeList = filter(
                lambda p: p.ParamType == paramType, normalizeParamList)
            isNameShouldBeNormalze = any(p.Name == name for p in paramTypeList)
            if isNameShouldBeNormalze is True:
                return ''
            return name
        except Exception as ex:
            logging.exception(ex)

    def __extractPasteDate(self, pasteSpecificPageTree):
        try:
            pasteDate = pasteSpecificPageTree.xpath(
                '//div[@class="date"]/span/text()')
            date_str = self.__trimDates(pasteDate[0])
            formatedDate = datetime.strptime(
                date_str, '%b %d, %Y').strftime('%Y-%m-%d')
            return formatedDate
        except Exception as e:
            logging.exception(e)

    def __trimDates(self, date_str):
        return re.sub(
            r"([0123]?[0-9])(st|th|nd|rd)", r"\1", date_str)

    def __extractPasteContent(self, pasteSpecificPageTree):
        try:
            pasteContentElement = pasteSpecificPageTree.xpath(
                '//div[@class="source"]')
            if pasteContentElement is not None:
                pasteContent = html.tostring(
                    pasteContentElement[0], pretty_print=True)
            return pasteContent.strip()

        except Exception as e:
            logging.exception(e)
