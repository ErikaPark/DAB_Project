import streamlit as st

from helper_functions import GetAllStations, GetStations

import networkx as nx


import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
#import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
#from folium import plugins 

class Window2:
    
    def __init__(self):
        super().__init__()
        self.tabs = st.session_state['choose']
    
    def create_window2(self):
        st.title("Exploratory Data Analysis")
       # self.draw_inputs()
        st.write("TODO")
        
   # def draw_inputs(self):
           # input_container = st.container()
           # crit_col, service_col = input_container.columns(2)
            # 구 별 장애인 인구 수 vs. 장애인 비율 
            
           # crit_input = crit_col.selectbox('인구 수 vs. 인구 비율', ('장애인 인구 수', '장애인 비율'))
           # service_input = service_col.selectbox('편의시설', ('충전기 대수', '리프트'))





