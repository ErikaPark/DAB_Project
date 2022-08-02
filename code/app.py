from st_on_hover_tabs import on_hover_tabs
import streamlit as st
from window1 import Window1
from window2 import Window2
from window3 import Window3
from window4 import Window4

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc


font_name = 'AppleGothic'
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False



def initialize():
        st.set_page_config(layout="wide")
        st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
        if 'df' not in st.session_state:
                st.session_state['df'] = False
        #st.session_state['1_8역간거리'] = pd.read_csv("../data/서울교통공사_1-8호선 역간거리 및 소요시간_20220111.csv",encoding='cp949',index_col=0)

        with st.sidebar:
                st.header('DAB 경진대회: 지하철 길찾기')
                st.session_state['choose'] = on_hover_tabs( tabName=['데이터 보기','EDA', '길찾기(기본)', '길찾기(휠체어)'], 
                             iconName=['journal', 'journal', 'train', 'bi-battery-charging'],
                             styles = {'navtab': {'background-color':'#111',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                       'tabOptionsStyle': {':hover :hover': {'color': 'red',
                                                                      'cursor': 'pointer'}},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'7.5px',
                                                    'text-align': 'left'},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'}},
                             key="1")


if __name__=="__main__":
        initialize()
        window1 = Window1()
        window2 = Window2()
        window3 = Window3()
        window4 = Window4()
        if st.session_state['choose'] == '데이터 보기': #1페이지 이동
                window1.create_window1()
        elif st.session_state['choose'] == 'EDA': #2페이지 이동
                window2.create_window2()       
        elif st.session_state['choose'] == '길찾기(기본)': #3페이지 이동 
                window3.create_window3()
        elif st.session_state['choose'] == '길찾기(휠체어 이용자)': #4페이지 이동 
                window4.create_window4()




