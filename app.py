# for running 
# python -m  streamlit run Flights_Dashboard\app.py

from cProfile import label
from anyio import value
import streamlit as st
import plotly.graph_objects as go


st.sidebar.title("flight Analysis")
user_option=st.sidebar.selectbox("Menu", [ "Analysis","CHeck Flight","Select One" ])

from dbhelper import DB
db = DB()

if user_option == "CHeck Flight":
    st.title("Flight Check")
    col1,col2=st.columns(2)
    cities=db.fetch_city_names()
    with col1:
        source = st.selectbox("Source",cities )
    with col2:
        destination = st.selectbox("Destination", cities)

    if st.button("Check Flights"):
        if source and destination:
            st.write(f"Checking flights from {source} to {destination}...")
            all_flight=db.fetch_all_flights(source,destination)
            st.write("Flight data will be displayed here.")
            st.dataframe(all_flight)
        else:
            st.error("Please select both source and destination.")
elif user_option ==  "Analysis":
    st.title("Flight Analysis")
    airline,freqL=db.fetch_flight_frequency()
    fig = go.Figure(data=[go.Pie(labels=airline, values=freqL, hole=0.3)])
    st.header("Flight Frequency Analysis")
    st.plotly_chart(fig)

    

    airport,freqP=db.fetch_busy_airport()
    print(airport,freqP)
    fig=go.Figure(data=[go.Bar(x=airport, y=freqP, text=freqP, textposition='auto')])
    fig.update_layout(title_text='Busy Airports', xaxis_title='Airports', yaxis_title='Frequency')
    st.header("Busy_Airport BAR Chart")
    st.plotly_chart(fig)

    st.header("Flight Data by Date")
    datesF,freqD=db.fetch_flight_date()
    fig = go.Figure(data=[go.Line(x=datesF, y=freqD, mode='lines+markers', name='Flight Frequency')])
    fig.update_layout(title_text='Flight Frequency by Date', xaxis_title='Date', yaxis_title='Frequency')
    st.plotly_chart(fig)

    dates= db.fetch_dates()
    date=st.selectbox("Select Date", dates)
    if date:
        st.write(f"Displaying flight data for {date}...")
        filtered_flights = db.fetch_flight_by_date(date)
        st.dataframe(filtered_flights)
    else:
        st.error("Please select a date to view flight data.")

    
    
    
elif user_option == "Select One":
    st.write("This section will contain flight analysis features.")

    st.write("Please select an option from the sidebar to proceed.")
