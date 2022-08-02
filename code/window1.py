import streamlit as st
import pandas as pd 
import plotly.express as px
from st_aggrid import AgGrid
from st_aggrid import grid_options_builder
import helper_functions 
import io
import matplotlib.pyplot as plt
from matplotlib import rc

from io import BytesIO
from google.oauth2 import service_account
from google.cloud import storage

font_name = 'AppleGothic'
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


# #google cloud 사용해서 데이터 받아옴
# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"]
# )
# storage_client = storage.Client(credentials=credentials)
# bucket_name = 'dab_streamlit_bucket'

# bucket = storage_client.get_bucket(bucket_name)
# blob_names = [blob.name for blob in bucket.list_blobs()]

s = st.session_state

class Window1:
    def __init__(self):
        super().__init__()
        self.amenities = pd.read_csv('../Data2/amenities.csv')
        self.census = pd.read_csv('../Data2/census_summary.csv')
        self.elevator = pd.read_csv('../Data2/elevator_move.csv')
        # self.transfer = self.load_csv('../Data2/서울교통공사_환승역거리 소요시간 정보_20210701.csv', 'kor')
        # self.len_transf_stn = self.load_excel('../Data2/역간 거리 및 소요시간_220730.xlsx', 'kor')
        # self.route_intn = self.load_excel('../Data2/역내이동동선.xlsx', 'kor')
        # self.charge_loc = self.load_csv('../Data2/역내충전소위치.csv', 'kor')
        # self.station_code = self.load_excel('../Data2/운영기관_역사_코드정보_2020.09.14.xlsx', 'kor')
        # self.station_info = self.load_csv('../Data2/지하철정보.csv', 'kor')
        # self.master_location = self.load_excel('../Data2/Master_location.xlsx', 'eng')
        # self.station_coordinate = self.load_csv('../Data2/station_coordinate.csv', 'eng')
        # self.district_loc = self.load_csv('../Data2/district_location.csv', 'eng')
    
    # def load_csv(self, filename, lang): 
    #     if lang == 'eng':
    #         df = pd.read_csv(filename, sep = ',', low_memory=False)
    #     elif lang == 'kor':
    #        df = pd.read_csv(filename, sep = ',',low_memory=False)
    #     return df

    # def load_excel(self, filename, lang):
    #     #blob = bucket.blob(filename)
    #     #data = blob.download_as_string()
    #     if lang == 'eng':
    #         df = pd.read_excel(filename)
    #     elif lang == 'kor':
    #         df = pd.read_excel(filename)
    #     return df
        

    def create_window1(self):
        st.write('<p style="font-size:130%">Choose Dataset</p>', unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns([0.5, 2, 0.1, 2, 0.5])

        file = c2.selectbox(label = 'Select Dataset', options= ['amenities.csv', 'census_summary.csv', 'elevator_move.csv'])
        self.get_df(file)

        c4.write("Import Dataset")
        file_format = c4.radio('Select file format:', ('csv', 'excel'), key='file_format')
        dataset = c4.file_uploader(label = '')
        if dataset:
            if file_format == 'csv':
                s['df'] = pd.read_csv(dataset)
            else:
                s['df'] = pd.read_excel(dataset)
            self.display_df(dataset)
            

        st.subheader('Choose Visualization Option')
        self.draw_inputs()

        
    def get_df(self, file):
        if file == 'amenities.csv':
            s['df'] =  self.amenities
        elif file == 'census_summary.csv':
            s['df'] = self.census
        elif file == 'elevator_move.csv':
            s['df'] = self.elevator   
        # elif file == '서울교통공사_환승역거리 소요시간 정보':
        #     s['df'] = self.transfer  
        # elif file == '역간 거리 및 소요시간':
        #     s['df'] = self.len_transf_stn
        # elif file ==  '역내이동동선.xlsx':
        #     s['df'] =  self.route_intn
        # #elif file == '역내충전소위치.csv':
        #  #   s['df'] = self.charge_loc
        # elif file == '운영기관_역사_코드정보.xlsx':
        #     s['df'] =  self.station_code
        # elif file == '지하철정보.csv':
        #     s['df'] =  self.station_info
        # elif file == 'Master_location.xlsx':
        #     s['df'] = self.master_location 
        # elif file == 'station_coordinate.csv':
        #     s['df'] =  self.station_coordinate
        # elif file == 'district_location.csv':
        #     s['df'] =  self.district_loc


        self.display_df(file)

    def display_df(self, filename):
        st.subheader('Display Chosen File: '+ filename)
        n = len(s['df']); m =len(s['df'].columns)
        st.write(f'<p style="font-size:130%">rows: {n}, columns: {m}</p>', unsafe_allow_html=True)
        gb = grid_options_builder.GridOptionsBuilder.from_dataframe(s['df']) 
        gb.configure_pagination(enabled=True)
        gb.configure_default_column(groupable = True) #변수 별로 그룹핑 가능하게 하기

        gridoptions = gb.build()
        AgGrid(s['df'], gridOptions = gridoptions)


    #def df_information(self, file): pass 
        #TODO
        # 갹 데이터의 짧막한 설명 쓰기 

    def draw_inputs(self):
        df = s['df']
        #option1
        options = ['Data Type Info', 'NA값 개수/비율', 'Count Plots']
        c1, c2, c3 = st.columns([0.5, 2, 0.5])
        option_input = c2.multiselect("", options)
        helper_functions.space(3)
        
        if 'Data Type Info' in option_input: 
            self.data_type_info(df)
            helper_functions.space(2)

        if 'NA값 개수/비율' in option_input: 
            self.count_NA(df)
            helper_functions.space(2)

        if 'Count Plots' in option_input:
            cat_columns = df.select_dtypes(include = 'object').columns
            st.subheader('Count/Distribution Plots of Selected Columns')
            if len(cat_columns) == 0:
                st.write('There is no categorical columns in the data.')
            else:
                #container = st.container(2)
                c1, c2, c3 = st.columns([0.5, 2, 0.5])
               
                select_all_button = c2.checkbox("Select all for plots")

                if select_all_button:
                    selected_num_cols = c2.multiselect('Choose columns for plots:',  cat_columns, default = list(cat_columns))
                else:
                    selected_num_cols = c2.multiselect('Choose columns for plots:',cat_columns, default = cat_columns[0])
                
                selected_cat_cols = selected_num_cols

                
                self.draw_plots(selected_cat_cols, df)
            helper_functions.space(2)
                



    def data_type_info(self, data):
        st.subheader("변수 별 Data Type 정보:")
        c1, c2, c3 = st.columns([1, 2, 1])
        c2.dataframe(self.df_info(data))

    def df_info(self,df):
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
    
    def count_NA(self, data):
        st.subheader('변수 별 NA 개수와 비율(%):')
        if data.isnull().sum().sum() == 0:
            st.write('There is not any NA value in your dataset.')
        else:
            c1, c2, c3 = st.columns([0.5, 2, 0.5])
            c2.dataframe(helper_functions.df_isnull(data), width=1500)
            helper_functions.space(2)

    def draw_plots(self, columns, df):
        i = 0
        while (i < len(columns)):
            c1, c2 = st.columns(2)
            for j in [c1, c2]:
                if (i >= len(columns)):
                    break
                fig = px.histogram(df, x = columns[i], color_discrete_sequence=['indianred'])
                j.plotly_chart(fig)
                i += 1
