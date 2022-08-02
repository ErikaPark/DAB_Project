import streamlit as st
import pandas as pd
#import numpy as np 
import io


#global data = pd.read_csv("../data/서울교통공사_1-8호선 역간거리 및 소요시간_20220111.csv",encoding='cp949',index_col=0)

class GetStations:
    def __init__(self, line_no):
        self.line_no = line_no
        self.get_stn(line_no)
        
    def get_stn(self, line_no):
        data = st.session_state['1_8역간거리']
        temp_df = data[data['호선'] == line_no]
        stations = list(temp_df.loc[:, '역명'])
        return stations 

    
class GetAllStations:
    def __init__(self):
        self.data = st.session_state['1_8역간거리']
    def get_stn(self):
        l = list(self.data.loc[:,'역명'])
        return l

def df_info(df):
    df.columns = df.columns.str.replace(' ', '_')
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()

    df_info = s.split('\n')

    counts = []
    names = []
    nn_count = []
    dtype = []
    for i in range(5, len(df_info)-3):
        line = df_info[i].split()
        counts.append(line[0])
        names.append(line[1])
        nn_count.append(line[2])
        dtype.append(line[4])

    df_info_dataframe = pd.DataFrame(data = {'#':counts, 'Column':names, 'Non-Null Count':nn_count, 'Data Type':dtype})
    return df_info_dataframe.drop('#', axis = 1)

def df_isnull(df):
    res = pd.DataFrame(df.isnull().sum()).reset_index()
    res['Percentage'] = round(res[0] / df.shape[0] * 100, 2)
    res['Percentage'] = res['Percentage'].astype(str) + '%'
    return res.rename(columns = {'index':'Column', 0:'Number of null values'})

def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

def multiselect_container(massage, arr, key):

    container = st.container()
    select_all_button = st.checkbox("Select all for " + key + " plots")
    if select_all_button:
        selected_num_cols = container.multiselect(massage, arr, default = list(arr))
    else:
        selected_num_cols = container.multiselect(massage, arr, default = arr[0])

    return selected_num_cols
