import streamlit as st
import pandas as pd

##
st.write("Klasifikasi Penerimaan Pengajuan Kredit")

# object
person_home_ownership = st.selectbox("person_home_ownership",
                                     ("RENT", "MORTGAGE", "OWN", "OTHER"),
                                     index=None,
                                     placeholder="select option")
loan_intent = st.selectbox("loan_intent",
                            ("EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"),
                            index=None,
                            placeholder="select option")
loan_grade = st.selectbox("loan_grade", ##### bisa gantiin loan status
                            ("A", "B", "C", "D", "E", "F", "G"),
                            index=None,
                            placeholder="select option")
cb_person_default_on_file = st.selectbox("cb_person_default_on_file",
                            ("Y", "N"),
                            index=None,
                            placeholder="select option")

# numerik
person_age = st.number_input("person_age",
                             min_value=0, #
                             max_value=100, 
                             value=None) #

person_income = st.number_input("person_income",
                                min_value=0, #
                                max_value=100, #
                                value=None)

person_emp_length = st.number_input("person_emp_length",
                             min_value=0.0, #
                             max_value=100.0, 
                             value=None) #

loan_amnt = st.number_input("loan_amnt",
                             min_value=0, #
                             max_value=100, 
                             value=None) #

loan_int_rate = st.number_input("loan_int_rate",
                             min_value=0.0, #
                             max_value=100.0, 
                             value=None) #

loan_percent_income = st.number_input("loan_percent_income",
                             min_value=0.0, #
                             max_value=100.0, 
                             value=None) #

cb_person_cred_hist_lenght = st.number_input("cb_person_cred_hist_lenght",
                             min_value=0, #
                             max_value=100, 
                             value=None) #


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
        "cb_person_cred_hist_lenght": cb_person_cred_hist_lenght
    }
    
    @st.dialog("Hasil Prediksi")
    def program(val):
        st.write(df)

    if "program" not in st.session_state:
        df = pd.DataFrame(input_dict, index=[0])
        program(df)