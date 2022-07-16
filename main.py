import streamlit as st
import pandas as pd
import sqlite3

connection =sqlite3.connect("data/f1.db")

st.title('FormulaWeb')


def get_race_results():
    race_results_df = pd.read_sql("select r.position as Position, d.forename || ' ' || d.surname as Name, "
                                  "c.name as Constructor, r.points as Points from results r inner JOIN "
                                  "drivers d on r.driverId=d.driverId "
                                  "inner join constructors c "
                                  "on c.constructorId=r.constructorId "
                                  "order by r.raceId desc limit 20;",connection)
    race_results_df['Points'] = race_results_df['Points'].astype(int)
    race_results_df['Position'] = race_results_df['Position'].astype(str)
    # print(race_results_df[race_results_df['Position']=="\\N"].loc[:,"Position"])
    # race_results_df[race_results_df['Position']=="\\N"].loc[:, 'Position'] = "DNF"
    race_results_df.loc[race_results_df['Position']=="\\N",'Position'] = "DNF"
    print(race_results_df)
    pd.options.display.float_format = '{:,.0f}'.format
    race_results_df.set_index('Position', drop = False,inplace=True)
    return race_results_df


data_load_state = st.text("Loading data..")
race_results = get_race_results()
data_load_state.text("Done!")
st.write("This is a sample streamlit app")
st.table(race_results)
