"""
MySQL client module
"""

import warnings

import pymysql


class Client():
    """
    MySQL client
    """
    def __init__(self, host, user, password, database):
        """
        Init function for class Client

        Args:
            host (str): database host
            user (str): username for database
            password (str): password for database user
            database (str): database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_all_books(self, table="books"):
        """
        Get all books from the database:

        Args:
            table (str): table to query the books from

        Returns:
            list of dicts: book titles and their authors
        """

        data = None
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                sql = "SELECT `author`, `title` FROM `%s`" % table
                cursor.execute(sql)
                data = cursor.fetchall()
                if data == ():
                    warnings.warn("data returned is empty", UserWarning)

        except connection.Error as err:
            print(err)
        except cursor.Error as err:
            print(err)
        finally:
            connection.close()

        return data

    def get_author_books(self, author, table="books"):
        """
        Get the book rows corresponding to the given author.

        Args:
            author (str): author name to search for
            table (str): optional, table to query from,

        Returns:
            list of dicts: books (ID, title, author)
        """

        data = None
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                sql = "SELECT `title` FROM `%s` WHERE author='%s'" % (
                    table,
                    author,
                )
                cursor.execute(sql)
                data = cursor.fetchall()
                if data == ():
                    warnings.warn(
                        ("data returned is empty. Author '%s' not found" %
                         author), UserWarning)
        except connection.Error as err:
            print(err)
        except cursor.Error as err:
            print(err)

        finally:
            connection.close()

        return data

    def get_book_row(self, title, table="books"):
        """
        Get the book row corresponding to the given title.

        Args:
            title (str): the title of the book to search for
            table (str): optional, the table to query in

        Returns:
            list of dicts: book row (ID, title, author)
        """

        data = None
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                sql = "SELECT `*` FROM `%s` WHERE `title`=\"%s\"" % (
                    table,
                    title,
                )
                cursor.execute(sql)
                data = cursor.fetchall()
                if data == ():
                    warnings.warn(
                        ("data returned is empty. Book '%s' not found" %
                         title), UserWarning)

        except connection.Error as err:
            print(err)
        except cursor.Error as err:
            print(err)

        finally:
            connection.close()

        return data

    def get_book_author(self, title):
        """
        Search for the author of a book.

        Args:
            title (string): title of the book

        Returns:
            string: the author of the book
        """

        book_row = self.get_book_row(title)

        if book_row is None or len(book_row) < 1:
            return ""

        return book_row[0]["author"]
