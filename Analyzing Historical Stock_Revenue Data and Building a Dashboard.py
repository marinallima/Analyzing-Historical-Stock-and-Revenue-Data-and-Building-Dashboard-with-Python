#!/usr/bin/env python
# coding: utf-8

# # Project Analyzing Historical Stock/Revenue Data and Building a Dashboard by Marina Lima

# # Extracting and Visualizing Stock Data

# In[2]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install pandas')
get_ipython().system('pip install requests')
get_ipython().system('pip install bs4')
get_ipython().system('pip install plotly')


# # Importando as bibliotecas

# In[3]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# # Question 1: Use yfinance to Extract Tesla Stock Data

# In[4]:


tesla = yf.Ticker("TSLA")


# In[5]:


tesla_data = tesla.history(period="max")


# In[6]:


tesla_data.reset_index(inplace=True)
tesla_data.head(5)


# #  Question 2: Use Webscraping to Extract Tesla Revenue Data

# In[7]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"


# In[8]:


html_data = requests.get(url).text


# In[9]:


soup = BeautifulSoup(html_data, "html.parser")
soup.find_all('title')


# In[13]:


tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")
    
    tesla_revenue_list.append(pd.DataFrame({"Date": [date], "Revenue": [revenue]}))

tesla_revenue = pd.concat(tesla_revenue_list, ignore_index=True)


# In[14]:


tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[16]:


tesla_revenue.tail(5)


# # QUESTION 3

# Reset the index, save, and display the first five rows of the gme_data dataframe using the head function. Upload a screenshot of the results and code from the beginning of Question 1 to the results below.

# In[17]:


gamestop = yf.Ticker("GME")


# In[18]:


gamestop_data = gamestop.history(period="max")


# In[19]:


gamestop_data.reset_index(inplace=True)
gamestop_data.head(5)


# # Question 4: Use Webscraping to Extract GME Revenue Data

# Display the last five rows of the gme_revenue dataframe using the tail function. Upload a screenshot of the results.

# In[20]:


url1 = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"


# In[21]:


html_data = requests.get(url1).text


# In[22]:


soup = BeautifulSoup(html_data, "html.parser")
soup.find_all('title')


# In[ ]:


import pandas as pd

gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):
    try:
        if 'GameStop Quarterly Revenue' in table.find('th').text:
            rows = table.find_all('tr')

            for row in rows:
                cols = row.find_all('td')

                if cols:
                    date = cols[0].text.strip()
                    revenue = cols[1].text.strip().replace(',', '').replace('$', '')

                    gme_revenue = gme_revenue.append({"Date": date, "Revenue": revenue}, ignore_index=True)
    except AttributeError:
        pass


# In[26]:


gme_revenue.tail(5)


# # Question 5: Plot Tesla Stock Graph

# ## Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph.

# In[27]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[28]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[29]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# # Question 6: Plot GameStop Stock Graph

# ## Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph.

# In[30]:


make_graph(gamestop_data, gme_revenue, 'GameStop')


# In[ ]:




