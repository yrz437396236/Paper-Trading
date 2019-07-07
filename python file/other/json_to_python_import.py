import pandas as pd
RDSA_1y60m = pd.read_json('C:\\Users\\43739\\OneDrive\\us\\2019 spring\\paper trading\\rdsa-1yr-60min-intraday.json')
RDSA_2y240m = pd.read_json('C:\\Users\\43739\\OneDrive\\us\\2019 spring\\paper trading\\rdsa-2yr-240min-intraday.json')
BP_1y60m = pd.read_json('C:\\Users\\43739\\OneDrive\\us\\2019 spring\\paper trading\\bp-1yr-60min-intraday.json')
BP_2y240m = pd.read_json('C:\\Users\\43739\\OneDrive\\us\\2019 spring\\paper trading\\bp-2yr-240min-intraday.json')

print(RDSA_1y60m)
RDSA_1y60m_df=pd.DataFrame(RDSA_1y60m)
RDSA_1y60m_df.index=RDSA_1y60m_df['date']
del(RDSA_1y60m_df['date'])
print([RDSA_1y60m_df])

cols = list(RDSA_1y60m_df)
cols.insert(0,cols.pop(cols.index('open')))
cols.insert(1,cols.pop(cols.index('high')))
cols.insert(2,cols.pop(cols.index('low')))
RDSA_1y60m_df = RDSA_1y60m_df.loc[:,cols]
RDSA_1y60m_df.to_csv('C:\\Users\\43739\\OneDrive\\us\\2019 spring\\paper trading\\rdsa-1yr-60min-intraday.csv')