import pandas as pd
from sklearn.preprocessing import minmax_scale

def processing(data):
    """
    data : data berupa dataframe pandas

    Fungsi melakukan pemrosesan data agar sesuai untuk input model
    """
    # buat loan-to-income ratio
    data['loan_to_income_ratio'] = data['loan_amnt'] / data['person_income']

    # buat loan-to-employment length ratio
    data['loan_to_emp_length_ratio'] =  data['person_emp_length']/ data['loan_amnt']

    # buat interest rate-to-loan amount ratio
    data['int_rate_to_loan_amt_ratio'] = data['loan_int_rate'] / data['loan_amnt']

    # buat list berdasarkan nilai kategori
    merge_ohe_col = [
        'N', 'Y', 'MORTGAGE', 'OTHER', 'OWN', 'RENT', 'DEBTCONSOLIDATION',
       'EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE'
    ]

    # buat list kategori
    ohe_colums = ['cb_person_default_on_file', 'person_home_ownership','loan_intent']

    # buat kolom dan data baru berdasarkan nilai kategori
    for category in merge_ohe_col:
        data[category] = 0.0
        for col in ohe_colums:
            if str(category) in str(data[col]):
                data[category] = 1.0

    # hapus kolom kategori
    data = data.drop(ohe_colums, axis=1)

    # buat urutan kolom menyesuaikan input untuk model
    new_col = ['N', 'Y', 'MORTGAGE', 'OTHER', 'OWN', 'RENT', 'DEBTCONSOLIDATION',
       'EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE',
       'person_age', 'person_income', 'person_emp_length', 'loan_amnt',
       'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length',
       'loan_to_income_ratio', 'loan_to_emp_length_ratio',
       'int_rate_to_loan_amt_ratio']
    data = data[new_col]
    
    # buat dict dan dataframe untuk nilai maksimum dan minimum data
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

    # gabungkan data dengan data_min_max
    data = pd.concat([data, min_max_df], axis=0)

    # normalisasis data
    data = minmax_scale(data.astype('float32'))

    # kembalikan data pertama
    return data[0]