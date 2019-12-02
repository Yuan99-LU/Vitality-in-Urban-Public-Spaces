import os
import pandas as pd

#txt_names = [x for x in os.listdir('./Lund_together/') if (x.endswith('.jpg'))]

#sort_names = sorted(txt_names)


D1=pd.read_csv("Stadsparken-Lund_Skane_County2.csv", header = None)
D2=pd.read_csv("Stadsparken-Lund_Skane_County.csv", header = None)
#print(D1[0:8])
D3 = D2.iloc[-13:]
D4 = pd.concat([D1, D3])
#print(D2)

D4.to_csv("Stadsparken-Lund_Skane_County3.csv", index=False, header=None)

