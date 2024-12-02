import pandas as pd
import numpy as np

# fungsi testing ELM
def elm_predict(X, W, b, round_output=False):
  """
  X           : Data
  W           : Bobot
  b           : Bobot keluaran
  round_output: Menentukan hasil berupa bilangan bulat atau tidak

  Fungsi melakukan pengujian dengan metode ELM
  Fungsi hasil prediksi
  """
  Hinit = X @ W.T
  H = 1 / (1 + np.exp(-Hinit))

  y = H @ b

  if round_output:
    y = int(round(y))
    if y > 1:
       y = 1
    elif y < 0:
      y = 0

  return y