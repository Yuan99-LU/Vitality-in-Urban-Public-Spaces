import os
import pandas as pd

#txt_names = [x for x in os.listdir('./Lund_together/') if (x.endswith('.jpg'))]

#sort_names = sorted(txt_names)


D1=pd.read_csv("Lund_University_Main_Building-Lund_Skane_County_copy.csv", header = None)
print(D1[0:8])
D1 = D1.drop(D1.index[[0, 1, 2, 3, 4, 5, 6, 7]])

D1.to_csv("Lund_University_Main_Building-Lund_Skane_County_delete_addtional_lines.csv", index=False, header=None)

