
import mysql.connector
# Connect to the MySQL database

class DB:
    def __init__(self):
        try:
            self.conn=mysql.connector.connect(
                host="localhost",
                user="root",    
                password="",
                database="flights_db"
            )
            self.mycursor=self.conn.cursor()
            print("Connected to the database successfully")
        except mysql.connector.errors as error:
            print(f"Failed to connect to the database: {error}")
            exit(1)

    def fetch_city_names(self):
        city=[]
    
        self.mycursor.execute("""
        SELECT DISTINCT(Source) FROM flight 
        union
        SELECT DISTINCT(Destination) FROM flight 
        """)
        data = self.mycursor.fetchall()
        for row in data:
            city.append(row[0])

        return city
    def fetch_all_flights(self,source,destination):
        self.mycursor.execute(f"""
        SELECT Airline,Route,Dep_Time,Duration,Price FROM flight
        WHERE Source='{source}' and Destination='{destination}'
        """)
        data=self.mycursor.fetchall();
        return data
    def close_connection(self):
        if self.conn.is_connected():
            self.mycursor.close()
            self.conn.close()
            print("Database connection closed.")
        else:
            print("No active database connection to close.")

    def fetch_flight_frequency(self):
        airline=[]
        freq=[]
        self.mycursor.execute("""
        SELECT Airline,Count(*) FROM flight
        GRoup By Airline
        """)
    
        data = self.mycursor.fetchall()

        for row in data:
            airline.append(row[0])
            freq.append(row[1])
        return airline,freq
    
    def fetch_busy_airport(self):
        airport=[]
        freq=[]
        self.mycursor.execute("""SELECT Source,COUNT(*) FROM (SELECT Source FROM flight
                                                             union all
                                                             SELECT Destination FROM flight) t
                                group by t.Source
                                order by COUNT(*) DESC """)
        busy=self.mycursor.fetchall()
        for row in busy:
            airport.append(row[0])
            freq.append(row[1])
        return airport,freq
    
    def fetch_dates(self):
        dates = []
        self.mycursor.execute("Select distinct(Date_of_Journey) from flight")
        data = self.mycursor.fetchall()
        for row in data:
            dates.append(row[0])

        return dates
    
    def fetch_flight_by_date(self, date):
        self.mycursor.execute(f"""
        SELECT Airline,Route,Dep_Time,Duration,Price FROM flight
        WHERE Date_of_Journey='{date}'
        """)
        data = self.mycursor.fetchall()
        return data
    def fetch_flight_date(self):
        self.mycursor.execute("""Select Date_of_Journey,COUNT(*) from flight
                                 group by Date_of_Journey""")
        data = self.mycursor.fetchall()
        dates = []
        freq = []  
        for row in data:
            dates.append(row[0])
            freq.append(row[1])
        return dates, freq

