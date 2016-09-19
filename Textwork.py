'''
This module is built on a class basses meaning all of the content
of this module is contained within classes. This module is the 'hub' of
the entire application. This is the only module that knows how to communicate
with all of the other modules, this allows for a nice and safe abstraction
barrier between all of the other modules.
Besides communicating and error checking, this module does not
do that much. However, it does contain the blueprint for the main representation of
what the data passed between each module should look like.

@author = Zachary
'''
import random

import SqlDataBase as sdb
import Internet as inter

class TextObject:

    def __init__(self, text=''):
        '''The base class, not implemented much but
        inherited by other classes'''

        # Make sure the text is a string
        assert isinstance(text, str), "Text Must be a string"
        self.body = text

    def convert(self, text):
        '''converts to a list for processing'''
        return text.split()

    def name_similarity(self, character):
        '''Asks the database for similar words'''
        if len(character) > 0:
            similar = sdb.list_similar(character)
            return ', '.join(similar)
        return ""

    def add_text(self, text):
        '''adds just the name to the database'''
        print("Adding: ", text)
        sdb.add_name(text)

    def __len__(self):
        return len(self.convert(self.body))

    def head(self):
        '''returns up to the first three words'''
        if len(self.body) >= 3:
            return (' '.join(self.convert(self.body)[:3]) + '...')
        return (self.body + '...')

    def __repr__(self):
        return 'TextObject({})'.format(self.head())

    def __str__(self):
        return self.body

class NamedText(TextObject):

    def __init__(self, name, text=''):
        '''Inherits from TextObject but does the bulk of the work
        is the main class used by the application GUI'''

        # Finish __init__ from TextObject
        self.__init__ = TextObject.__init__(self, text)
        # Convert the text body into a list
        # This allows for easier processing later
        # Also allows for multi-line look up of words
        self._name = [na.lower() for na in name]
        # Checks to see if a definition was passed
        # If no definition was passed, converts
        # checks again to see if it was multi word
        # the creates a definition in the appropriate manner
        if len(text) <= 0:
            if isinstance(self.name, str):
                self.text = self.return_definition(self.name)
            else:
                self.text = self.build_text(self.name)

    # Used to distinguish between mult-word
    # and single word name attributes
    @property
    def name(self):
        '''the name attribute'''
        if len(self._name) <= 1:
            return self._name[0]
        else:
            return self._name

    def add_all(self):
        '''creates a new definition with name and body'''
        sdb.add_defintion(self.name, self.body)

    def return_definition(self, text):
        '''Returns the definition from the database or internet'''
        print(text)
        db_def = self.db_defin(text)
        if db_def:
            print(text,"Was Found in the dataBase")
            return db_def
        else:
            print(text, "Was Requested from the internet")
            new_def = self.inter_defin(text)
            sdb.add_defintion(text, new_def)
            return new_def

    def build_text(self, lis):
        '''Builds the string that is returned to the main GUI'''
        return_str = ""
        for i in lis:
            bot_str = '{}:\n{}\n\n'.format(i, self.return_definition(i))
            return_str += bot_str
        return return_str


    def db_defin(self, text):
        '''asks for a definition from the database'''
        definition = sdb.find_definition(text)
        if definition:
            return definition
        else:
            return False

    def inter_defin(self, text):
        '''asks the internet module for a definition'''
        return inter.grab_definition(text)

    def __repr__(self):
        return 'NamedText({}:{})'.format(self.name, self.body)

class SqlConnection:

    # Stored ID Tokens
    token_data_base = []

    def __init__(self):
        '''Main object that interacts with the SQL Data Base
        and is used by the GUI to close and open connections'''

        # Creates a token for ID purposes
        self.token = random.randrange(100)
        # Checks to make sure Token is unique
        self.check_token()

    def check_token(self):
        '''Checks token against token data base'''
        if self.token in SqlConnection.token_data_base:
            while self.token in SqlConnection.token_data_base:
                self.token = random.randrange(100)
            SqlConnection.token_data_base.append(self.token)
        return self.token

    def inilalize(self):
        '''Opens a connection in the SQL data base'''
        sdb.prepare_main()
        return "Data Base Created"

    def display(self, setting=0):
        '''Asks the SQL DB for the contents of one
        of the data base or both'''
        # Creates a new function to access the DB
        # This is mainly done for abstraction but
        # will likely be taken out in the future
        def get_list():
            nonlocal setting
            assert setting < 3 and setting >= 0, "Cannot set the 'setting attribute to that value'"
            if setting == 0:
                command = ("name",)
            elif setting == 1:
                command = ("definition",)
            else:
                command = ("name", "definition")
            return sdb.display_database(*command)
        to_process = get_list()
        if isinstance(to_process, tuple):
            return "None"
        else:
            return ', '.join(to_process)

    def clean(self, setting=0):
        '''cleans the data for doubles'''
        pass

    def close(self, on=True):
        '''Closes the SQL Connection '''
        if on:
            sdb.close()

    def __repr__(self):
        return "Connection: {}".format(self.token)


def main():
    sp = SqlConnection()
    sp.inilalize()
    print(sp.display(setting=0))
    sp.close()


if __name__ == "__main__":main()






