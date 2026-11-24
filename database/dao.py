from database.DB_connect import DBConnect
from model.filiale import Filiale
from model.collegamento import Collegamento

class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    @staticmethod
    def get_filiali():
        cnx = DBConnect.get_connection()
        if cnx is None:
            print ("Errore di connessione al database.")
            return None
        filiali = {}
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM filiale"""
        try:
            cursor.execute(query)
            for row in cursor:
                filiale = Filiale(
                    id = row["id"],
                    codice = row["codice"],
                    nome = row["nome"],
                    citta = row["citta"],
                    provincia = row["provincia"],
                    latitudine=row["latitudine"],
                    longitudine=row["longitudine"],
                )
                filiali[filiale.id] = filiale
        except Exception as e:
            print(f"Errore durante la query delle filiali. {e}")
            filiali = None
        finally:
            cursor.close()
            cnx.close()
        return filiali

    @staticmethod
    def get_collegamenti():
        cnx = DBConnect.get_connection()
        if cnx is None:
            print ("Errore di connessione al database.")
            return None
        collegamenti = []
        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT
                    LEAST (id_filiale_origine, id_filiale_destinazione) AS f1,
                    GREATEST(id_filiale_origine, id_filiale_destinazione) AS f2,
                    AVG(importo) AS importo_medio
                FROM bonifico
                GROUP BY f1, f2
                """
        try:
            cursor.execute(query)
            for row in cursor:
                collegamenti.append((row["f1"], row["f2"], float(row["importo_medio"])))
        except Exception as e:
            print(f"Errore durante la query dei collegamenti. {e}")
            collegamenti = None
        finally:
            cursor.close()
            cnx.close()
        return collegamenti