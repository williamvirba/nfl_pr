#!/usr/bin/env python
# coding: utf-8

# In[207]:


# In[206]:


import nfl_data_py as nfl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


# In[105]:


ty = list(range(2022,2022+1))
dfyr=nfl.import_pbp_data(years=ty) # YR Input must be list or range thats why []


# In[106]:


dfyruq=list(dfyr["passer_player_name"].unique())
dfyruq.remove(None)


# In[167]:


wk=list(dfyr["week"].unique())


# In[172]:


objwp={}
maxprp=2.375
minprp=0
condition1=[lambda x: x >=minprp and x<=maxprp  ]
condition2=[lambda x: x>2.375  ]
condition3=[lambda x: x<0 ]
wk=wk[0:-1]

for i in dfyruq:
    objwp[str(i)]=list()
    for w in wk :

            dfyrw = dfyr[dfyr["week"] == w]
            
            
            pa=dfyrw[dfyrw["passer_player_name"] == i]["pass_attempt"].sum()-dfyrw[dfyrw["passer_player_name"] == i]["sack"].sum()
            co=dfyrw[dfyrw["passer_player_name"] == i]["complete_pass"].sum() 
            py=dfyrw[dfyrw["passer_player_name"] == i]["passing_yards"].sum() 
            tp=dfyrw[dfyrw["passer_player_name"] == i]["pass_touchdown"].sum() 
            ip=dfyrw[dfyrw["passer_player_name"] == i]["interception"].sum() 
            
            if pa<=5 :
               pr=None
            else:
            
                a=((co/pa)-0.3)*5
                b=((py/pa)-3)*0.25
                c=((tp/pa))*20
                d=(maxprp-((ip/pa)*25))
    
                abcd=[a,b,c,d]
                abcde=[]
            
            

                for para in abcd :


                    if all(func(para) for func in condition1):
                        abcde.append(para)
              
                    elif any(func(para) for func in condition2):
                        para = 2.375
                        abcde.append(para)
            
                    elif any(func(para) for func in condition3):
                        para = 0
                        abcde.append(para)
            
            
                pr=((sum(abcde))/6)*100
            
    
                objwp[str(i)].append(pr)
            
objwp

#qbjs=qbj.sort_values(qbj.columns[0],ascending=False) # nefunguje nedefinované iba ako upravena kopia

#qbjs


# In[194]:


qbjw = pd.DataFrame.from_dict(objwp, orient='index',columns=wk)
qbjw=qbjw.sort_values(qbjw.columns[0],ascending=False)
#qbjw.fillna(0).values.mean(axis=1)
qbjw


# In[197]:


qbjwt=qbjw.T
qbjwt


# In[116]:


qbjw10=qbjwt.iloc[: , :32]


# In[117]:


qbp = qbjw10.plot(kind="line")


# In[177]:


fig, ax = plt.subplots(figsize=(19, 16))
ax.set_ylim([0, 158.3])
ax.set_title('Passer rating of passers')
qbp = ax.plot(qbjwt)


# In[204]:


figs = px.line(qbjwt)
figs.update_traces(visible="legendonly")
figs.data[0].visible=True
figs.data[1].visible=True
figs


# In[205]:


st.show(figs)

