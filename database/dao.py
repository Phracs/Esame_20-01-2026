from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artists_with_soglia(a:int):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select a.id
from artist a, album al
where a.id=al.artist_id 
group by a.id 
having count(distinct al.id)>=%s"""
        cursor.execute(query, (a,))
        for row in cursor:
            result.append(row["id"])
        cursor.close()
        conn.close()
        return result



    @staticmethod
    def get_archi_with_peso():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """with artist_genre as(select g.id as genre_id, a.id as artist_id
					from track t, album al, genre g, artist a
					where t.genre_id=g.id 
and t.album_id= al.id 
and al.artist_id= a.id)
select ag1.artist_id as a1, ag2.artist_id as a2, count(distinct ag1.genre_id) as weight 
from artist_genre ag1, artist_genre ag2
where ag1.genre_id=ag2.genre_id
and ag1.artist_id < ag2.artist_id
group by ag1.artist_id, ag2.artist_id """
        cursor.execute(query)
        for row in cursor:
            result.append((row["a1"], row["a2"], row["weight"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nomi_da_id(id:int):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select a.id, a.name
                   from artist a
                   where a.id =%s"""
        cursor.execute(query, (id,))
        for row in cursor:
            result.append((row["id"], row["name"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_peso_from_archi(a1, a):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """with artist_genre as (select g.id as genre_id, a.id as artist_id 
                                         from track t, 
                                              album al, 
                                              genre g, 
                                              artist a 
                                         where t.genre_id = g.id 
                                           and t.album_id = al.id 
                                           and al.artist_id = a.id)
                   select ag1.artist_id as a1, ag2.artist_id as a2, count(distinct ag1.genre_id) as weight
                   from artist_genre ag1, 
                        artist_genre ag2
                   where ag1.genre_id = ag2.genre_id
                     and ag1.artist_id = %s
                    and ag2.artist_id = %s
                   group by ag1.artist_id, ag2.artist_id"""
        cursor.execute(query, (a1, a))
        for row in cursor:
            result.append((row["a1"], row["a2"], row["weight"]))
        cursor.close()
        conn.close()
        return result