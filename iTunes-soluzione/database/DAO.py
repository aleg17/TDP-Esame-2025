from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAlbums(dMin):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary = True)

        query = """ SELECT a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds)/1000/60 as dTot
                        from album a, track t
                        where a.AlbumId = t.AlbumId 
                        GROUP BY a.AlbumId 
                        HAVING dTot > %s """

        cursor.execute(query, (dMin,)) # in minuti

        results = []
        for row in cursor:
            results.append(Album(**row))

        cursor.close()
        cnx.close()
        return results

    @staticmethod
    def getAllEdges(idMapAlbum):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary = True)

        query = """SELECT DISTINCTROW t1.AlbumId as a1, t2.AlbumId as a2 
                    FROM track t1, track t2, playlisttrack p1, playlisttrack p2
                    WHERE t2.TrackId = p2.TrackId 
                    and t1.TrackId = p1.TrackId
                    and p2.PlaylistId = p1.PlaylistId
                    and t1.AlbumId < t2.AlbumId 
                     """

        cursor.execute(query) # in minuti

        results = []
        for row in cursor:
            if row["a1"] in idMapAlbum and row["a2"] in idMapAlbum:
                results.append((idMapAlbum[row["a1"]], idMapAlbum[row["a2"]]))

        cursor.close()
        cnx.close()
        return results