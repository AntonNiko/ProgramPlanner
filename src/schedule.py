import datetime
from aenum import MultiValueEnum
from enum import Enum
import jsonschema


class Schedule():
    """
    Represents a container for a term and its sections, spanning a date range.
    """

    def __init__(self):
        self.activeSections = {}

    def addSection(self, courseName, section):
        """
        Adds a section to the list of active sections. Conflict resolution is not performed
        here.
        """

        if courseName not in self.activeSections:
            self.activeSections[courseName] = {}
        self.activeSections[courseName][section.name] = section

    def removeSection(self, courseName, section):
        """
        Removes a section from the list of active sections.
        """

        del self.activeSections[courseName][section.name]
        if len(self.activeSections[courseName]) == 0:
            del self.activeSections[courseName]

    def doesSectionConflict(self, sectionToCompare):
        """
        Given a `Section` object, determines if the section conflicts with any 
        of the active sections
        """

        for section in self.activeSections:
            if self.activeSections[section].doesSectionConflict(sectionToCompare):
                return True
        return False
        