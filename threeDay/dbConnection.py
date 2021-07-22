import psycopg2
import psycopg2.extras
import pandas as pd

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "lelwd"
DB_USER = "postgres"
DB_PASS = "Mwpmwp2622"


# connect to the db
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
)


# cursor
cur = conn.cursor()

conn.autocommit = True


def create_staging_table(cursor):
    cursor.execute(
        """DROP TABLE IF EXISTS threeday CASCADE;\
        CREATE
        UNLOGGED TABLE threeday (
            hourEnd         INTEGER,
            MWvalue         INTEGER,
        )
        """
    )


with conn.cursor() as cursor:
    create_staging_table(cursor)


def send_csv_to_psql(connection, csv, table_):
    sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
    file = open(csv, "r")
    table = table_
    with connection.cursor as cur:
        cur.execute("turncate " + table + ";")  # avoid duplicated
        cur.copy_expert(sql=sql % table, file=file)
        cur.close()
        conn.close()
    return connection.commit()


# we will use a csv file made in another file
send_csv_to_psql(conn, "csv file name", "threeday")

sql_ = "SELECT COUNT(*) FROM threeday"
cur.execute(sql_)
cur.fetchall()


# cur.execute("insert into threeday (id, max) values (%s, %s)", (2, 20))

# execute the query
# cur.execute("select id, max from threeday")

# rows = cur.fetchall()

# for r in rows:
#     print(f"id {r[0]} max {r[1]}")

# commit changes to the db
# conn.commit()


# copy data from the csv to postgres
f = open(r"C:\Users\matth\python.files\lelwd\LELWD\test.csv", "r")
cur.copy_from(f, temp_unicommerce_status, sep=",")
f.close()

# close the cursor
cur.close()


# close the connection
conn.close()