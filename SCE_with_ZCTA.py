
# coding: utf-8

# In[366]:

import pandas as pd
import os
import numpy as np


# In[367]:

path = os.getcwd() + '\SCE Spreadsheet Data'
print(path)
files = os.listdir(path)
print(files)


# In[368]:

main_df = pd.DataFrame
older_dfs = []
older_files = [f for f in files if ".xls" in f and ("2014" in f or "2015" in f or "2016" in f)]
print(older_files)
current_dfs = []
for f in older_files:
    xls = pd.ExcelFile('SCE Spreadsheet Data/' + f)
    df = xls.parse('Sheet1', skiprows=0, index_col=None, na_values=['NA'])
    print(len(df))
    older_dfs.append(df)

main_df = pd.concat(older_dfs)


# In[369]:

converter = pd.ExcelFile('SCE Spreadsheet Data/' + 'zip_to_zcta_2018.xlsx')


# In[370]:

converter = converter.parse('ziptozcta2017', skiprows=0, index_col=None, na_values=['NA'])


# In[371]:

headers = converter.iloc[0]
# converter  = pd.DataFrame(converter.values[1:], columns=headers)


# In[372]:

#rint(converter['ZIP_CODE'])
for x in converter['ZIP_CODE']:
    print(x)


# In[373]:

new_zips = []
for x in converter['ZIP_CODE']:
    if len(str(x)) == 3:
        new_zips.append('00' + str(x))
    elif len(str(x)) == 4:
        new_zips.append('0' + str(x))
    else:
        new_zips.append(x)
        
converter['ZIP_CODE'] = new_zips


# In[374]:

test = pd.ExcelFile('SCE Spreadsheet Data/' + 'SCE_2017_Q1_ElectricUsageByZip.xls')
test = test.parse('Sheet1', skiprows=0, index_col=None, na_values=['NA'])


# In[375]:

test.rename(columns = {"Zip\nCode": "ZIP_CODE", }, 
                                 inplace = True) 


# In[376]:

out = pd.merge(test, converter)


# In[377]:

census_data = pd.read_csv('SCE Spreadsheet Data/' + '2016_5YR_ZCTA.csv')


# In[378]:

ztca_codes = []
for x in census_data['Geo_QName']:
    ztca_codes.append(x[0:5])


# In[379]:

census_data['ZCTA'] = ztca_codes


# In[380]:

result = pd.merge(out, census_data)


# In[381]:

out2 = out[['ZIP_CODE','ZCTA']]


# In[382]:

codes1 = main_df['Zip\nCode'].values
codes2 = main_df['Zip Code'].values


# In[383]:

for i in range(len(codes2)):
    curr = codes2[i]
    if type(curr) != int:
        codes2[i] = codes1[i]


# In[384]:

for i in range(len(codes1)):
    curr = codes1[i]
    if type(curr) != int:
        codes1[i] = codes2[i]


# In[385]:

main_df['Zip\nCode'] = codes1


# In[386]:

main_df.drop(['Zip\nCode'], axis=1)


# In[387]:

main_df = main_df.drop(['Zip\nCode'], axis=1)


# In[388]:

main_df = main_df.drop(['Zip\nBlock', 'Zip Block'], axis=1)


# In[389]:

cc1 = main_df['Customer\nClass'].values
cc2 = main_df['Customer Class'].values


# In[390]:

for i in range(len(cc2)):
    curr = cc2[i]
    if type(curr) != str:
        cc2[i] = cc1[i]


# In[391]:

main_df['Customer Class'] = cc2


# In[392]:

main_df = main_df.drop( 'Customer\nClass', axis = 1)


# In[393]:

out2.rename(columns={'ZIP_CODE':'Zip Code'}, 
                 inplace=True)


# In[394]:

final = pd.merge(main_df, out2)


# In[395]:

export_csv = final.to_csv (path + '\\final.csv') #Don't forget to add '.csv' at the end of the path


# In[396]:

print(path)


# In[397]:

final.head()


# In[398]:

main_df = pd.DataFrame
older_dfs = []
older_files = [f for f in files if ".xls" in f and ("2017" in f or "2018" in f) and not("zcta" in f)]
print(older_files)
current_dfs = []
for f in older_files:
    xls = pd.ExcelFile('SCE Spreadsheet Data/' + f)
    df = xls.parse('Sheet1', skiprows=0, index_col=None, na_values=['NA'])
    print(len(df))
    older_dfs.append(df)

main_df = pd.concat(older_dfs)


# In[399]:

second_df = main_df.drop(['Unnamed: 1',
 'Unnamed: 2',
 'Unnamed: 3',
 'Unnamed: 4',
 'Unnamed: 5',
 'Unnamed: 6',
 'Unnamed: 7',
 'Usage Aggregation by Zip code for Web Posting'], axis=1)


# In[400]:

codes1 = second_df['Average kWh'].values
codes2 = second_df['AveragekWh'].values


# In[401]:

for i in range(len(codes1)):
    curr = codes1[i]
    if (curr == codes1[0]):
        if codes2[i] > 0:
            codes1[i] = codes2[i]
    curr2 = codes2[i]
    if (curr2 == codes1[0]):
        if codes1[i] > 0:
            codes2[i] = codes1[i]

second_df['Average kWh'] = codes1
second_df['AveragekWh'] = codes2


# In[402]:

second_df = second_df.drop(['Average kWh'], axis=1)


# In[403]:

second_df.head()


# In[406]:

nullTotalAccounts1 = second_df['Total Accounts'].isnull().values
nullTotalAccounts2 = second_df['TotalAccounts'].isnull().values

codes1 = second_df['Total Accounts'].values
codes2 = second_df['TotalAccounts'].values

for i in range(len(nullTotalAccounts1)):
    if (nullTotalAccounts1[i] == True) and (nullTotalAccounts2[i] == False):
        codes1[i] = codes2[i]
    if (nullTotalAccounts2[i] == True) and (nullTotalAccounts1[i] == False):
        if (type(codes1[i]) != str):
            codes2[i] = codes1[i]
        
second_df['Total Accounts'] = codes1
second_df['TotalAccounts'] = codes2


# In[407]:

second_df = second_df.drop(['Total Accounts'], axis=1)


# In[408]:

second_df.head()


# In[409]:

nullTotalAccounts1 = second_df['Total kWh'].isnull().values
nullTotalAccounts2 = second_df['TotalkWh'].isnull().values

codes1 = second_df['Total kWh'].values
codes2 = second_df['TotalkWh'].values

for i in range(len(nullTotalAccounts1)):
    if (nullTotalAccounts1[i] == True) and (nullTotalAccounts2[i] == False):
        codes1[i] = codes2[i]
    if (nullTotalAccounts2[i] == True) and (nullTotalAccounts1[i] == False):
        if (type(codes1[i]) != str):
            codes2[i] = codes1[i]
        
second_df['Total kWh'] = codes1
second_df['TotalkWh'] = codes2


# In[410]:

second_df = second_df.drop(['Total kWh'], axis=1)


# In[411]:

final.head()


# In[412]:

second_df = second_df.rename(columns = {'Customer\nClass' : 'Customer Class', 'Zip\nCode' : 'Zip Code'})


# In[413]:

second_df.head()


# In[414]:

final2 = pd.merge(second_df, out2)


# In[415]:

final2.head()


# In[416]:

final.head()


# In[417]:

final3 = final2.append(final)


# In[418]:

final3.head()


# In[421]:

export_csv = final.to_csv (path + '\\SCE_with_ZCTA.csv') #Don't forget to add '.csv' at the end of the path

