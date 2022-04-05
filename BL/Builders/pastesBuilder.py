
from BL.Builders.builderBase import BuilderBase
from Dal.Models.pasteModel import PasteModel
from lxml import html
from datetime import datetime
import re
from SharedResourses.logService import LogService


class PasteBuilder(BuilderBase):

    def __init__(self) -> None:
        try:
            super().__init__()
            self.logger = LogService()
        except Exception as e:
            self.logger.error(e)

    # decalre the paste model data extraction process step by step
    def Build(self, pasteSpecificPageTree, normalizeParamList):
        try:
            paste = PasteModel()
            authorName = self.__extractPasteAuthor(pasteSpecificPageTree)

            # using a ready made list to replace values
            # which considered as "same meaning"
            paste.Author = self.__normalizeParam(
                normalizeParamList, authorName, 'Author')

            title = self.__extractPasteTitle(pasteSpecificPageTree)

            paste.Title = self.__normalizeParam(
                normalizeParamList, title, 'Title')

            paste.Date = self.__extractPasteDate(pasteSpecificPageTree)

            paste.Content = self.__extractPasteContent(pasteSpecificPageTree)

            return paste
        except Exception as e:
            self.logger.error(e)

    def __extractPasteTitle(self, pasteSpecificPageTree):
        try:
            pasteTitle = pasteSpecificPageTree.xpath(
                '//div[@class="info-top"]/h1/text()')
            return pasteTitle[0]
        except Exception as e:
            self.logger.error(e)

    def __extractPasteAuthor(self, pasteSpecificPageTree):
        try:
            pasteAuthor = pasteSpecificPageTree.xpath(
                '//div[@class="username"]/a/text()')
            return pasteAuthor[0]
        except Exception as e:
            self.logger.error(e)

    def __normalizeParam(self, normalizeParamList, value, paramType):
        try:
            # filter normalizeParamList by paramType
            # ex:Author or Title from list

            paramTypeList = filter(
                lambda p: p.ParamType == paramType, normalizeParamList)

            isValueShouldBeNormalze = any(
                p.Name == value for p in paramTypeList)

            # if value exist in list it should be normalized
            if isValueShouldBeNormalze is True:
                return ''
            return value
        except Exception as e:
            self.logger.error(e)

    def __extractPasteDate(self, pasteSpecificPageTree):
        try:
            pasteDate = pasteSpecificPageTree.xpath(
                '//div[@class="date"]/span/text()')

            # dates in pastes.com are in format: 'April 4th ,2022'
            # we need to remove the day ending
            # ex: 4th,2nd,3rd to create legal date
            date_str = self.__trimDates(pasteDate[0])

            formatedDate = datetime.strptime(
                date_str, '%b %d, %Y').strftime('%Y-%m-%d')

            return formatedDate
        except Exception as e:
            self.logger.error(e)

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
            self.logger.error(e)
