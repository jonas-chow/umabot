from commands.stamina.track import Track, Condition, Race
from psycopg2 import connect

def get_cm_track(dbUrl):
    conn = connect(dbUrl, sslmode = 'require')
    cur = conn.cursor()

    cur.execute("SELECT * FROM races WHERE user_id = 0")
    race = cur.fetchone()
    race = race_from_query(race)
    cur.close()
    conn.close()
    return race

def get_user_track(dbUrl, user_id):
    conn = connect(dbUrl, sslmode = 'require')
    cur = conn.cursor()

    cur.execute("SELECT * FROM races WHERE user_id = %s", (user_id,))
    race = cur.fetchone()

    # fetch cm if user has no race registered
    if race is None:
        cur.execute("SELECT * FROM races WHERE user_id = 0")
        race = cur.fetchone()
    
    race = race_from_query(race)
    cur.close()
    conn.close()
    return race

def set_user_track(dbUrl, user_id, race: Race):
    distance = race.distance
    type = race.type.value
    condition = race.condition.value

    conn = connect(dbUrl, sslmode = 'require')
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO races VALUES (%s, %s, %s, %s) 
        ON CONFLICT (user_id) DO 
        UPDATE SET distance = %s, type = %s, condition = %s WHERE races.user_id = %s
        """, (user_id, distance, type, condition, distance, type, condition, user_id))
    
    conn.commit()
    cur.close()
    conn.close()

def race_from_query(race):
    distance = race[1]
    type = Track(race[2])
    condition = Condition(race[3])
    return Race(distance, type, condition)