import pandas as pd
#import numpy as np
#from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import minmax_scale,StandardScaler
#import streamlit as st

def processing(data):
    # hapus loan_grade
    #data.drop(['loan_grade'], axis=1)

    # buat loan-to-income ratio
    data['loan_to_income_ratio'] = data['loan_amnt'] / data['person_income']

    # buat loan-to-employment length ratio
    data['loan_to_emp_length_ratio'] =  data['person_emp_length']/ data['loan_amnt']

    # buat interest rate-to-loan amount ratio
    data['int_rate_to_loan_amt_ratio'] = data['loan_int_rate'] / data['loan_amnt']

    merge_ohe_col = [
        'N', 'Y', 'MORTGAGE', 'OTHER', 'OWN', 'RENT', 'DEBTCONSOLIDATION',
       'EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE'
    ]

    ohe_colums = ['cb_person_default_on_file', 'person_home_ownership','loan_intent']

    for category in merge_ohe_col:
        data[category] = 0.0
        for col in ohe_colums:
            if str(category) in str(data[col]):
                data[category] = 1.0

    #data = data.drop(ohe_colums, axis=1)
    """
    ohe = OneHotEncoder()
    ohe.fit(data[ohe_colums])

    # Menggabungkan kategori dengan cara yang lebih aman
    merge_ohe_col = []
    for categories in ohe.categories_:
        merge_ohe_col.extend(categories)

    merge_ohe_col = np.array(merge_ohe_col)  # Menyusun kategori menjadi satu array
    #print("Total kategori: ", len(merge_ohe_col))

    # Memeriksa jika kolom memiliki lebih dari 1 kategori
    ohe_colums = [col for col, categories in zip(ohe_colums, ohe.categories_) if len(categories) > 1]

    # Refit OneHotEncoder jika ada kolom yang tidak valid
    ohe.fit(data[ohe_colums])

    merge_ohe_col = np.array([
        'N', 'Y', 'MORTGAGE', 'OTHER', 'OWN', 'RENT', 'DEBTCONSOLIDATION',
       'EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE']
    )
    ohe_transform =  ohe.transform(data[ohe_colums]).toarray()

    ####
    st.write(ohe_transform)
    st.write(merge_ohe_col)

    ohe_data = pd.DataFrame(ohe_transform, columns=merge_ohe_col)
    """
    new_col = ['N', 'Y', 'MORTGAGE', 'OTHER', 'OWN', 'RENT', 'DEBTCONSOLIDATION',
       'EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE',
       'person_age', 'person_income', 'person_emp_length', 'loan_amnt',
       'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length',
       'loan_to_income_ratio', 'loan_to_emp_length_ratio',
       'int_rate_to_loan_amt_ratio']
    
    #data = pd.concat([ohe_data, data], axis=1)
    data = data.drop(ohe_colums, axis=1)
    data = data[new_col]

    normal_col = ['person_income','person_age','person_emp_length', 'loan_amnt','loan_int_rate','cb_person_cred_hist_length','loan_percent_income', 'loan_to_emp_length_ratio',
        'int_rate_to_loan_amt_ratio']

    #scaler_normal = StandardScaler()
    #data.loc[:,normal_col] = scaler_normal.fit_transform(data.loc[:,normal_col])
    
    min_max_dict = {
        'N': [1.0, 0.0], 
        'Y': [1.0, 0.0], 
        'MORTGAGE': [1.0, 0.0], 
        'OTHER': [1.0, 0.0], 
        'OWN': [1.0, 0.0], 
        'RENT': [1.0, 0.0], 
        'DEBTCONSOLIDATION': [1.0, 0.0],
        'EDUCATION': [1.0, 0.0],
        'HOMEIMPROVEMENT': [1.0, 0.0], 
        'MEDICAL': [1.0, 0.0], 
        'PERSONAL': [1.0, 0.0],
        'VENTURE': [1.0, 0.0],
        'person_age': [65, 22],
        'person_income': [6000000, 4000], 
        'person_emp_length': [38.0, 0.0], 
        'loan_amnt': [35000, 500],       
        'loan_int_rate': [23.22, 5.42], 
        'loan_percent_income': [0.83, 0.0], 
        'cb_person_cred_hist_length': [30, 2],
        'loan_to_income_ratio': [35000 / 6000000, 500 / 4000], 
        'loan_to_emp_length_ratio': [38.0 / 35000, 0.0 / 500],
        'int_rate_to_loan_amt_ratio': [23.22 / 35000, 5.42 / 500]
    }
    min_max_df = pd.DataFrame(min_max_dict)
    data = pd.concat([data, min_max_df], axis=0)
    data = minmax_scale(data.astype('float32'))

    return data[0]