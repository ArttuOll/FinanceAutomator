from pymysql import DatabaseError, connect


class Dao:
    """Huolehtii tietokantaan kirjoittamisesta ja sieltä lukemisesta."""
    def __init__(self, address, username, password, database):
        self.address = address
        self.username = username
        self.password = password
        self.database = database

    def write_settings(self, transactions_dir, save_dir):
        """Kirjoittaa annetut asetukset tietokantaan. Tällä hetkellä ainoa
        asetus on tilitapahtumat sisältävän tiedoston sijainti
        (muuttuja directory)."""

        connection = connect(self.address, self.username, self.password,
                                     self.database)

        cursor = connection.cursor()
        try:
            # Poistetaan edelliset asetukset ennen uusien tallentamista.
            cursor.execute("DELETE FROM settings;")
            cursor.execute("INSERT INTO settings VALUES (%s, %s)", (transactions_dir, save_dir))
            connection.commit()
        except DatabaseError as error:
            print(error.args)
            print("Nothing was saved")
            connection.rollback()

        connection.close()

    def read_settings(self):
        """Lukee asetukset tietokannasta ja palauttaa ne yhtenä muuttujana."""

        connection = connect(self.address, self.username, self.password, self.database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM settings;")

        settings = cursor.fetchone()
        connection.close()

        return settings
