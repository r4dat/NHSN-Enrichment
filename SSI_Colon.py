# -*- coding: utf-8 -*-
'''
Created on Mon Sep 28 16:26:09 2015

@author: r4dat
'''

# ICD9 procs from NHSN definition.
# Diabetes diagnoses from AHRQ version 5 SAS program, CMBFQI32.TXT
# sample string generator print((','.join(map(str, [str(x) for x in range(25040,25094)]))).replace(',','","'))
#
#       "25000"-"25033",
#       "64800"-"64804" = "DM"        /* Diabetes w/o chronic complications*/
#       "25000","25001","25002","25003","25004","25005","25006","25007","25008","25009","25010","25011","25012","25013","25014","25015","25016","25017","25018","25019","25020","25021","25022","25023","25024","25025","25026","25027","25028","25029","25030","25031","25032","25033",
#       "64800","64801","64802","64803","64804"
#
#       "25040"-"25093",
#       "7751 " = "DMCX"              /* Diabetes w/ chronic complications */
#       "25040","25041","25042","25043","25044","25045","25046","25047","25048","25049","25050","25051","25052","25053","25054","25055","25056","25057","25058","25059","25060","25061","25062","25063","25064","25065","25066","25067","25068","25069","25070","25071","25072","25073","25074","25075","25076","25077","25078","25079","25080","25081","25082","25083","25084","25085","25086","25087","25088","25089","25090","25091","25092","25093"
#       "7751"
#

import pypyodbc
import pandas as pd
import numpy as np


pd.set_option('expand_frame_repr', False)

inpdb12 = pypyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\db12.accdb')
inpdb13 = pypyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\db13.accdb')
inpdb14 = pypyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\db14.accdb')
inpdb15 = pypyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\db15.accdb')

conn_dict = {2012: inpdb12,
             2013: inpdb13,
             2014: inpdb14,
             2015: inpdb15}

# Dictionary: each year has a tuple of names for the needed tables
# tables can be named differently each year
tablenames_dict = {2008: ['[ST08IP-DS1]', '[ST08IP-DS1DIAG]', '[ST08IP-DS1PROC]', '[ST08IP-DS1REV'],
                   2009: ['[ST09IP-4Q-DS1MAIN]', '[ST09IP-4Q-DS1DIAG]', '[ST09IP-4Q-DS1PROC]', '[ST09IP-4Q-DS1REV'],
                   2010: ['[ST2010IPDS1MAIN]', '[ST2010IPDS1DIAG]', '[ST2010IPDS1PROC]', '[ST2010IPDS1REV'],
                   2011: ['[ST2011Q4IPDS1MAIN]', '[ST2011Q4IPDS1DIAG]', '[ST2011Q4IPDS1PROC]', '[ST2011Q4IPDS1REV'],
                   2012: ['[ST2012Q4IPDS1]', '[ST2012Q4IPDS1DIAG]', '[ST2012Q4IPDS1PROC]', '[ST2012Q4IPDS1REV'],
                   2013: ['[ST2013Q4IPDS1MAIN]', '[ST2013Q4IPDS1DIAG]', '[ST2013Q4IPDS1PROC]', '[ST2013Q4IPDS1REV'],
                   2014: ['[ST2014Q4IPDS1]', '[ST2014Q4IPDS1DIAG]', '[ST2014Q4IPDS1PROC]', '[ST2014Q4IPDS1REV'],
                   2015: ['[ST2015Q1IPDS1]', '[ST2015Q1IPDS1DIAG]', '[ST2015Q1IPDS1PROC]', '[ST2015Q1IPDS1REV']}

###############################################################################
#                           DF processing
###############################################################################
cols_to_keep = ['CNTRL', 'HOSP', 'ZIP', 'DOB', 'SEX', 'ADATE','adate']

cols_to_keep = [x.lower() for x in cols_to_keep]


# Function to stack datasets according to discharge year
def make_main(iyear):
    for iteryear in conn_dict.keys():
        if iteryear == iyear:
            base_ds = pd.read_sql(
                ' '.join(['select * from', tablenames_dict[iteryear][0], 'where year(adate) =', str(iyear), ';']),
                conn_dict[iteryear])  # where year(adate) =',str(iyear)
            base_ds = base_ds[cols_to_keep]
            base_ds['orig_table'] = tablenames_dict[iteryear][0]
            base_ds['dbyear'] = iteryear
            record_count = len(base_ds)
            print(' '.join(
                ['file', tablenames_dict[iteryear][0], 'has', str(record_count), 'records with admit dates in',
                 'CY' + str(iyear)]))
        if iteryear > iyear:
            add_ds = pd.read_sql(
                ' '.join(['select * from', tablenames_dict[iteryear][0], 'where year(adate) =', str(iyear), ';']),
                conn_dict[iteryear])
            add_ds = add_ds[cols_to_keep]
            add_ds['orig_table'] = tablenames_dict[iteryear][0]
            add_ds['dbyear'] = iteryear
            record_count = len(add_ds)
            print(' '.join(
                ['file', tablenames_dict[iteryear][0], 'has', str(record_count), 'records with admit dates in',
                 'CY' + str(iyear)]))
            base_ds = pd.concat([base_ds, add_ds])
    return base_ds


def make_colo(iyear):
    for iteryear in conn_dict.keys():
        if iteryear == iyear:
            base_ds = pd.read_sql(' '.join([
                                               'select b.cntrl,proc,procdate,hosp,dob,sex,adate,ddate,ethn,race FROM (select distinct cntrl,proc,procdate from',
                                               tablenames_dict[iteryear][2], 'where year(procdate) =', str(iyear),
                                               " and proc IN('1731','1732','1734','1735','1736','1739', '4503', '4526', '4541','4549', '4552', '4571','4572','4573','4574','4575','4576', '4579', '4581','4582','4583', '4592','4593','4594','4595', '4603', '4604', '4610','4611', '4613', '4614', '4643', '4652', '4675','4676', '4694')",
                                               ') as a left join', tablenames_dict[iteryear][0],
                                               'as b ON a.cntrl=b.cntrl;']), conn_dict[iteryear])
            base_ds['orig_table'] = tablenames_dict[iteryear][2]
            base_ds['dbyear'] = iteryear
            record_count = len(base_ds)
            print(' '.join(
                ['file', tablenames_dict[iteryear][2], 'has', str(record_count), 'records with admit dates in',
                 'CY' + str(iyear)]))
        if iteryear > iyear:
            add_ds = pd.read_sql(' '.join([
                                              'select b.cntrl,proc,procdate,hosp,dob,sex,adate,ddate,ethn,race FROM (select distinct cntrl,proc,procdate from',
                                              tablenames_dict[iteryear][2], 'where year(procdate) =', str(iyear),
                                              " and proc IN('1731','1732','1734','1735','1736','1739', '4503', '4526', '4541','4549', '4552', '4571','4572','4573','4574','4575','4576', '4579', '4581','4582','4583', '4592','4593','4594','4595', '4603', '4604', '4610','4611', '4613', '4614', '4643', '4652', '4675','4676', '4694')",
                                              ') as a left join', tablenames_dict[iteryear][0],
                                              'as b ON a.cntrl=b.cntrl;']), conn_dict[iteryear])
            add_ds['orig_table'] = tablenames_dict[iteryear][2]
            add_ds['dbyear'] = iteryear
            record_count = len(add_ds)
            print(' '.join(
                ['file', tablenames_dict[iteryear][2], 'has', str(record_count), 'records with admit dates in',
                 'CY' + str(iyear)]))
            base_ds = pd.concat([base_ds, add_ds])
    return base_ds


def make_diab(iyear):
    for iteryear in conn_dict.keys():
        if iteryear == iyear:
            base_ds = pd.read_sql(' '.join(
                ['select a.cntrl,diag,adate,ddate FROM (select distinct cntrl,diag from', tablenames_dict[iteryear][1],
                 "WHERE diag IN('25000','25001','25002','25003','25004','25005','25006','25007','25008','25009','25010','25011','25012','25013','25014','25015','25016','25017','25018','25019','25020','25021','25022','25023','25024','25025','25026','25027','25028','25029','25030','25031','25032','25033','64800','64801','64802','64803','64804')",
                 ') as a LEFT JOIN', tablenames_dict[iteryear][0], 'as b ON a.cntrl=b.cntrl WHERE year(adate)=',
                 str(iyear), ';']), conn_dict[iteryear])
            base_ds['orig_table'] = tablenames_dict[iteryear][1]
            base_ds['dbyear'] = iteryear
            record_count = len(base_ds)
            print(' '.join(['file', tablenames_dict[iteryear][1], 'has', str(record_count), 'records with  Diab in',
                            'CY' + str(iyear)]))
        if iteryear > iyear:
            add_ds = pd.read_sql(' '.join(
                ['select a.cntrl,diag,adate,ddate FROM (select distinct cntrl,diag from', tablenames_dict[iteryear][1],
                 "WHERE diag IN('25000','25001','25002','25003','25004','25005','25006','25007','25008','25009','25010','25011','25012','25013','25014','25015','25016','25017','25018','25019','25020','25021','25022','25023','25024','25025','25026','25027','25028','25029','25030','25031','25032','25033','64800','64801','64802','64803','64804')",
                 ') as a LEFT JOIN', tablenames_dict[iteryear][0], 'as b ON a.cntrl=b.cntrl WHERE year(adate)=',
                 str(iyear), ';']), conn_dict[iteryear])
            add_ds['orig_table'] = tablenames_dict[iteryear][1]
            add_ds['dbyear'] = iteryear
            record_count = len(add_ds)
            print(' '.join(
                ['file', tablenames_dict[iteryear][1], 'has', str(record_count), 'records with Diab dates in',
                 'CY' + str(iyear)]))
            base_ds = pd.concat([base_ds, add_ds])
    return base_ds


def make_diabx(iyear):
    for iteryear in conn_dict.keys():
        if iteryear == iyear:
            base_ds = pd.read_sql(' '.join(
                ['select a.cntrl,diag,adate,ddate FROM (select distinct cntrl,diag from', tablenames_dict[iteryear][1],
                 "WHERE diag IN('25040','25041','25042','25043','25044','25045','25046','25047','25048','25049','25050','25051','25052','25053','25054','25055','25056','25057','25058','25059','25060','25061','25062','25063','25064','25065','25066','25067','25068','25069','25070','25071','25072','25073','25074','25075','25076','25077','25078','25079','25080','25081','25082','25083','25084','25085','25086','25087','25088','25089','25090','25091','25092','25093','7751')",
                 ') as a LEFT JOIN', tablenames_dict[iteryear][0], 'as b ON a.cntrl=b.cntrl WHERE year(adate)=',
                 str(iyear), ';']), conn_dict[iteryear])
            base_ds['orig_table'] = tablenames_dict[iteryear][1]
            base_ds['dbyear'] = iteryear
            record_count = len(base_ds)
            print(' '.join(['file', tablenames_dict[iteryear][1], 'has', str(record_count), 'records with DiabX in',
                            'CY' + str(iyear)]))
        if iteryear > iyear:
            add_ds = pd.read_sql(' '.join(
                ['select a.cntrl,diag,adate,ddate FROM (select distinct cntrl,diag from', tablenames_dict[iteryear][1],
                 "WHERE diag IN('25040','25041','25042','25043','25044','25045','25046','25047','25048','25049','25050','25051','25052','25053','25054','25055','25056','25057','25058','25059','25060','25061','25062','25063','25064','25065','25066','25067','25068','25069','25070','25071','25072','25073','25074','25075','25076','25077','25078','25079','25080','25081','25082','25083','25084','25085','25086','25087','25088','25089','25090','25091','25092','25093','7751')",
                 ') as a LEFT JOIN', tablenames_dict[iteryear][0], 'as b ON a.cntrl=b.cntrl WHERE year(adate)=',
                 str(iyear), ';']), conn_dict[iteryear])
            add_ds['orig_table'] = tablenames_dict[iteryear][1]
            add_ds['dbyear'] = iteryear
            record_count = len(add_ds)
            print(' '.join(
                ['file', tablenames_dict[iteryear][1], 'has', str(record_count), 'records with DiabX dates in',
                 'CY' + str(iyear)]))
            base_ds = pd.concat([base_ds, add_ds])
    return base_ds


# Interactive Test Frame
# test=pd.read_sql(' '.join(['select TOP 200 * from',tablenames_dict[2014][0]]),conn_dict[2014])
# print('Creating Main dataset')
# main13=make_main(2013)

## 2013
col13 = make_colo(2013)
diab = make_diab(2013)
diabx = make_diabx(2013)

col13['key'] = col13['cntrl'].map(int).map(str) + col13['dbyear'].map(str)
diab['key'] = diab['cntrl'].map(str) + diab['dbyear'].map(str)
diabx['key'] = diabx['cntrl'].map(str) + diabx['dbyear'].map(str)

col13['dm'] = col13['key'].isin(diab['key'])
col13['dmx'] = col13['key'].isin(diabx['key'])

col13 = col13.rename(columns=
{
    'hosp': 'ccn',
    'sex': 'gender',
    'adate': 'admitdate'
})

col13.drop_duplicates(subset=['key'], keep='first', inplace=True)
col13['dob'] = pd.to_datetime(col13['dob'])
col13['procdate'] = pd.to_datetime(col13['procdate'])
col13['ccn'] = col13['ccn'].map(int)
col13['admitdate'] = pd.to_datetime(col13['admitdate'])

## 2014
col14 = make_colo(2014)
diab = make_diab(2014)
diabx = make_diabx(2014)

col14['key'] = col14['cntrl'].map(int).map(str) + col14['dbyear'].map(str)
diab['key'] = diab['cntrl'].map(str) + diab['dbyear'].map(str)
diabx['key'] = diabx['cntrl'].map(str) + diabx['dbyear'].map(str)

col14['dm'] = col14['key'].isin(diab['key'])
col14['dmx'] = col14['key'].isin(diabx['key'])

col14 = col14.rename(columns=
{
    'hosp': 'ccn',
    'sex': 'gender',
    'adate': 'admitdate'
})

col14.drop_duplicates(subset=['key'], keep='first', inplace=True)
col14['dob'] = pd.to_datetime(col14['dob'])
col14['procdate'] = pd.to_datetime(col14['procdate'])
col14['ccn'] = col14['ccn'].map(int)
col14['admitdate'] = pd.to_datetime(col14['admitdate'])

colo_discharges = col13.append(col14, ignore_index=True)

all_proc = pd.read_csv(r"C:\All_Procedures_2013_2015.csv", header=0)
all_inf = pd.read_csv(r"C:\Line List - All Infection Events 2013-2015.csv", header=0)

colo_nhsn = all_proc[all_proc['procCode'] == 'COLO']
colo_nhsn.columns = map(str.lower, colo_nhsn.columns)
colo_nhsn['dob'] = pd.to_datetime(colo_nhsn['dob'])
colo_nhsn['procdate'] = pd.to_datetime(colo_nhsn['procdate'])
colo_nhsn['ccn'] = colo_nhsn['ccn'].map(int)

colo_inf = all_inf[all_inf['procCode'] == 'COLO']
colo_inf.columns = map(str.lower, colo_inf.columns)
colo_inf['dob'] = pd.to_datetime(colo_inf['dob'])
colo_inf['procdate'] = pd.to_datetime(colo_inf['procdate'])
colo_inf['ccn'] = colo_inf['ccn'].map(int)
colo_inf['admitdate'] = pd.to_datetime(colo_inf['admitdate'])

tmp = pd.merge(colo_nhsn, colo_discharges, how='left', on=['ccn', 'dob', 'gender', 'procdate'])
test = pd.merge(colo_inf, colo_discharges, how='left', on=['ccn', 'dob', 'gender', 'admitdate'])

tmp['DiabClm'] = np.nan
tmp['DiabClm'][(tmp['dm'].isin([True])) | (tmp['dmx'].isin([True]))] = 'Y'
tmp['DiabClm'][(tmp['dm'].isin([False])) & (tmp['dmx'].isin([False]))] = 'N'


# tmp.to_csv(r"C:\deterministic_match.csv")

def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(['Diabetic', 'Non-Diabetic']))
    plt.xticks(tick_marks, ['Diabetic', 'Non-Diabetic'], rotation=45)
    plt.yticks(tick_marks, ['Diabetic', 'Non-Diabetic'])
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


print("File output")
