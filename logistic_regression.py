import pandas.io.sql as psql
import sqlite3 as lite
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm
from pandas.core.common import isnull
from sklearn import linear_model
from pandas import Series, DataFrame, Index
from numpy import *
from sqlite3 import *
con = connect("restdata1.db")
conn1=connect("logicdata.db") 

c1 = conn1.cursor() 

c1.execute("DROP TABLE IF EXISTS LOGIC")

sql1 = """CREATE TABLE LOGIC (
         NAME  FLOAT,
		 DELIVERY FLOAT,
		 TAKEOUT FLOAT,
		 CREDITCARD FLOAT,
		 GOODFOR FLOAT,
		 PARKING FLOAT,
		 GOODFORKIDS FLOAT,
		 GOODFORGROUPS FLOAT,
		 ATTIRE FLOAT,
		 AMBIENCE FLOAT,
		 NOISELEVEL FLOAT,
		 ALCOHOL FLOAT,
		 OUTDOOR FLOAT,
		 HASTV FLOAT,
		 WAITERS FLOAT
		 )"""
	
c1.execute(sql1)

with con:
 	df1 = psql.read_frame('''SELECT NAME as N1, DELIVERY as Del1, TAKEOUT as TO1,CREDITCARD as CC1, GOODFOR as GF1, PARKING as Park1, GOODFORKIDS as GFK1, \
				GOODFORGROUPS as GFG1, ATTIRE as Attr1, AMBIENCE as Amb1, NOISELEVEL as NL1, ALCOHOL as Alc1,OUTDOOR as OD1, HASTV as TV1, WAITERS as WT1 from RESTAURANTS''',con)
	df = df1.ix[1:]
	df2 = psql.read_frame('''SELECT NAME as N2, DELIVERY as Del2, TAKEOUT as TO2,CREDITCARD as CC2, GOODFOR as GF2, PARKING as Park2,  GOODFORKIDS as GFK2, \
				GOODFORGROUPS as GFG2, ATTIRE as Attr2, AMBIENCE as Amb2, NOISELEVEL as NL2, ALCOHOL as Alc2,OUTDOOR as OD2,  HASTV as TV2, WAITERS as WT2 \
				from RESTAURANTS where NAME like "%Hong Hua"''',con)
	df_0=df2.ix[1:]

	def get_match(df,cat1,cat2):
		df_match = df[df[cat1].str.contains(cat2)]
		df_match['Match'] = np.ones(len(df_match))

		df_nomatch= df[~df[cat1].str.contains(cat2)]
		df_nomatch['Match'] = np.zeros(len(df_nomatch))
		df_merge = df_match.append(df_nomatch)
		columns = ['Del1', 'TO1', 'CC1', 'GF1', 'Park1','GFK1','GFG1','Attr1','Amb1','NL1','Alc1','OD1','TV1','WT1']
		X = columns
		return df_merge['N1'],df_merge['Match']

	def BuildX(df):
		columns = ['Del1', 'TO1', 'CC1', 'GF1', 'Park1','GFK1','GFG1','Attr1','Amb1','NL1','Alc1','OD1','TV1','WT1']
		X = np.ones(shape=(len(df),len(columns)+1))
		X[:,range(1,len(columns)+1)] = df[columns].values
		return X
	select_list = list(df.columns.values)
	my_list=list(df_0.columns.values)
	columns = ['Del1', 'TO1', 'CC1', 'GF1', 'Park1','GFK1','GFG1','Attr1','Amb1','NL1','Alc1','OD1','TV1','WT1']
	i=1
	y=np.empty((14,10))
	x=[]
	X=[]
	
	K = [[1 for x in xrange(10)] for x in xrange(14)]
	while i<len(my_list):
		cat2=df2.iloc[0][my_list[i]]
		cat1 = select_list[i]
		name,p= get_match(df,cat1,cat2)
		
		y[i-1]= p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]
		columns = ['Del1', 'TO1', 'CC1', 'GF1', 'Park1','GFK1','GFG1','Attr1','Amb1','NL1','Alc1','OD1','TV1','WT1']
		y=y
		uniques, x = np.unique(columns, return_inverse=True)
		X=np.array([x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13]])
		X=X
		f = 'y ~ x'
		logit = linear_model.LogisticRegression()
	
		logit.fit(y,X)
		i+=1
	logitscore = logit.score(y, X)