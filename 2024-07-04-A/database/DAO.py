from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select * 
                        from sighting s 
                        order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select distinct year(`datetime`) as years
                        from sighting s 
                        order by years desc  """
            cursor.execute(query)

            for row in cursor:
                if row["years"] not in result:
                    result.append(row["years"])
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllShapes(year: int):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ SELECT DISTINCT s.shape
                        FROM sighting s 
                        WHERE YEAR(s.datetime) = %s
                        ORDER BY shape ASC """
            cursor.execute(query, (year,))

            for row in cursor:
                # se il campo non è None, lo aggiungo alla lista
                if row["shape"] is not None and row["shape"] != "":
                    result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(year: int, shape: str):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select *
                        from sighting s 
                        where year(s.`datetime`) = %s
                            and s.shape = %s """
            cursor.execute(query, (year, shape))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(year: int, shape: str, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select t1.id as id1, t1.datetime as d1, t2.id as id2, t2.datetime as d2
                        from(   select * 
                                from sighting s  
                                where YEAR(`datetime`) = %s  
                                and shape = %s			) as t1,
                            (   select * 
                                from sighting s
                                where YEAR(`datetime`) = %s
                                and shape = %s			) as t2
                        where t1.state = t2.state and t1.datetime < t2.datetime
                        # trovare tutte le coppie di avvistamenti di forma "circle"
                        # nello stesso stato, ordinati nel tempo (cioè t1 avvenuto prima di t2) """
            cursor.execute(query, (year, shape, year, shape))

            for row in cursor:
                result.append((idMap[row["id1"]], idMap[row["id2"]]))
            cursor.close()
            cnx.close()
        return result