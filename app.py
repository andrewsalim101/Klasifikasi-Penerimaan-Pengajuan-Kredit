import streamlit as st
import pandas as pd
import numpy as np
from elm_predict import elm_predict
from data_processing import processing
#import os

##
st.write("Klasifikasi Penerimaan Pengajuan Kredit")

person_age = st.number_input("person_age",
                             min_value=22, 
                             max_value=65, 
                             value=None) 

person_income = st.number_input("person_income",
                                min_value=4000, 
                                max_value=6000000, 
                                value=None)

person_home_ownership = st.selectbox("person_home_ownership",
                                     ("RENT", "MORTGAGE", "OWN", "OTHER"),
                                     index=None,
                                     placeholder="select option")


person_emp_length = st.number_input("person_emp_length",
                             min_value=0.0, 
                             max_value=38.0, 
                             value=None) 

loan_intent = st.selectbox("loan_intent",
                            ("EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"),
                            index=None,
                            placeholder="select option")


loan_amnt = st.number_input("loan_amnt",
                             min_value=500, 
                             max_value=35000, 
                             value=None) #

loan_int_rate = st.number_input("loan_int_rate",
                             min_value=5.42, #
                             max_value=23.22, 
                             value=None) #

loan_percent_income = st.number_input("loan_percent_income",
                             min_value=0.0, 
                             max_value=0.83, 
                             value=None) 

cb_person_default_on_file = st.selectbox("cb_person_default_on_file",
                            ("Y", "N"),
                            index=None,
                            placeholder="select option")

cb_person_cred_hist_length = st.number_input("cb_person_cred_hist_length",
                             min_value=2, 
                             max_value=30, 
                             value=None) 


## simpan sebagai pandas
if st.button("Submit"):
    input_dict = {
        "person_home_ownership": person_home_ownership,
        "loan_intent": loan_intent,
        "cb_person_default_on_file": cb_person_default_on_file,
        "person_age": person_age,
        "person_income": person_income,
        "person_emp_length": person_emp_length,
        "loan_amnt": loan_amnt,
        "loan_int_rate": loan_int_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_cred_hist_length": cb_person_cred_hist_length
    }
    
    condition = True
    @st.dialog("Data belum terisi")
    def validasi():
        return False

    @st.dialog("Hasil Prediksi")
    def program(val):
        st.write(val)
    
    if "validasi" not in st.session_state:
        for key, val in input_dict.items():
            if val is None:
                condition = validasi()
                break

    if "program" not in st.session_state and condition:
        df = pd.DataFrame(input_dict, index=[0])

        W = np.load("elm_W.npy")
        b = np.load("elm_beta.npy")
        new_df = processing(df)
        output = elm_predict(new_df, W, b, round_output=True)

        #st.write(f"before {output}")
        if output == 0:
            output = 'diterima'
        elif output == 1:
            output = 'ditolak'

        #st.write(f"after {output}")
        program(f"Pengajuan peminjam: {output}")