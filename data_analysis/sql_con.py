import psycopg2
import pandas as pd

def db_conn(query):
    #database credentials
    PGHOST = 'localhost'
    PGDATABASE = 'mimic'
    PGUSER = 'postgres'
    PGPASSWORD = '' #fill in your password
    conn_string = "host="+ PGHOST +" port="+ "5432" +" dbname="+ PGDATABASE +" user=" + PGUSER \
                    +" password="+ PGPASSWORD
    
    try:                
        connection = psycopg2.connect(conn_string)
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")
        cur = connection.cursor()
        cur.execute(query)        
        rows = cur.fetchall()
        names = [ x[0] for x in cur.description]
        return(pd.DataFrame(rows, columns = names))
        
        
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        
    finally:
        #closing database connection.
            if(connection):
                cur.close()
                connection.close()
                print("PostgreSQL connection is closed")