import streamlit as st
import pandas as pd
import numpy as np
from elm_predict import elm_predict
from data_processing import processing

## masukkan data
st.write("Klasifikasi Penerimaan Pengajuan Kredit")

person_age = st.number_input("Usia peminjam",
                             min_value=20, 
                             max_value=65, 
                             value=None) 

person_income = st.number_input("Pendapatan tahunan (Rp)",
                                min_value=4000_000, 
                                max_value=6000000_000, 
                                value=None)

person_home_ownership = st.selectbox("Jenis kepemilikan tempat tinggal saat ini",
                                     ("Sewa", "KPR/kredit", "Pemilik", "Lainnya"),
                                     index=None,
                                     placeholder="pilih")


person_emp_length = st.number_input("Lama bekerja (tahun)",
                             min_value=0.0, 
                             max_value=60.0, 
                             value=None) 
                             
loan_intent = st.selectbox("Tujuan peminjaman",
                            ("Pendidikan", "Pengobatan", "Bisnis", "Pribadi", "Penggabungan_Utang", "Renovasi_Rumah"),
                            index=None,
                            placeholder="pilih")


loan_amnt = st.number_input("Jumlah pinjaman (Rp)",
                             min_value=500_000, 
                             max_value=35000_000, 
                             value=None) #

loan_int_rate = st.number_input("Suku bunga yang diajukan (tahun)",
                             min_value=5.42, 
                             max_value=23.22, 
                             value=None) 

loan_percent_income = st.number_input("Persentase pendapatan yang disisihkan untuk melunasi",
                             min_value=0.25, 
                             max_value=0.83, 
                             value=None) 

cb_person_default_on_file = st.selectbox("Pernah mengalami gagal bayar",
                            ("Iya", "Tidak"),
                            index=None,
                            placeholder="pilih")

cb_person_cred_hist_length = st.number_input("Lama peminjaman kredit (bulan)",
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
        "person_income": (person_income // 1_000),
        "person_emp_length": person_emp_length,
        "loan_amnt": (loan_amnt // 1_000),
        "loan_int_rate": loan_int_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_cred_hist_length": cb_person_cred_hist_length
    }
    
    condition = True
    @st.dialog("Data belum terisi")
    def validasi():
        st.write("Mohon isi data terlebih dahulu")
        return False

    @st.dialog("Hasil Pengajuan")
    def program(val):
        st.write(val)
    
    if "validasi" not in st.session_state:
        for key, val in input_dict.items():
            if val is None:
                condition = validasi()
                break

    if "program" not in st.session_state and condition:
        tempat_tinggal = { #person_home_ownership
            "Sewa":"RENT",
            "KPR/kredit": "MORTGAGE",
            "Pemilik": "OWN",
            "Lainnya": "OTHER"
        }
        tujuan = { #loan_intent
            "Pendidikan": "EDUCATION",
            "Pengobatan": "MEDICAL",
            "Bisnis": "VENTURE",
            "Pribadi": "PERSONAL",
            "Penggabungan_Utang": "DEBTCONSOLIDATION",
            "Renovasi_Rumah": "HOMEIMPROVEMENT"
        }
        gagal_bayar = { #cb_person_default_on_file
            "Iya": "Y",
            "Tidak": "N"
        }

        input_dict["person_home_ownership"] = tempat_tinggal[input_dict["person_home_ownership"]]
        input_dict["loan_intent"] = tujuan[input_dict["loan_intent"]]
        input_dict["cb_person_default_on_file"] = gagal_bayar

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
        program(f"Pengajuan peminjaman anda : {output}")