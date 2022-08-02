import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

class Window3:
    
    def __init__(self):
        super().__init__()
        self.tabs = st.session_state['choose']
    
    def create_window3(self):
        st.title("휠체어 사용자를 위한 길찾기 기능")
        st.write('Name of option is {}'.format(self.tabs))
