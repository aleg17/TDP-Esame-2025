//CHIAMATA DAO PER LISTA SEMPLICE NO PARAMETRI

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


//CHIAMATA DAO PER NODI E CONNESSIONI

    @staticmethod
    def getAllDriversbyYear(year):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """Select DISTINCT d.driverId as driverID, d.forename as name, d.surname as surname
				from drivers as d, races as r, results as re
				where r.year = %s
				and re.raceId = r.raceId
				and re.driverId = d.driverId
				and re.position is not null"""

        cursor.execute(query, (year,))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results
        

    @staticmethod
    def getDriverYearResults(year, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as d1, r2.driverId as d2, count(*) as cnt
				from results as r1, results as r2, races
				where r1.raceId = r2.raceId
				and races.raceId = r1.raceId
				and races.year = %s
				and r1.position is not null
				and r2.position is not null 
				and r1.position < r2.position 
				group by d1, d2"""

        cursor.execute(query, (year,))

        for row in cursor:
            results.append((idMap[row["d1"]],idMap[row["d2"]], row["cnt"]))

        cursor.close()
        conn.close()
        return results

//CHIAMATA DAO PER PESO DA UTILIZZARE SE IL GRAFO è PESATO E NON SI RIESCE
//A INSERIRE IL PESO NELLE CONNESSIONI
  
    @staticmethod
    def getPeso(forma,anno,stato1,stato2):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """select count(*) as peso
                    from sighting s 
                    where s.shape=%s and year(s.`datetime`)=%s and (s.state=%s or s.state=%s)
                     """

        cursor.execute(query,(forma,anno,stato1,stato2,))

        for row in cursor:
            result=row["peso"]

        cursor.close()
        conn.close()
        return result
