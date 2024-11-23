#---------------------------<><><><><><><><><><><><><><><><>---------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pandasai import SmartDataframe
from pandasai import Agent
from pandasai.ee.agents.semantic_agent import SemanticAgent
from pandasai.ee.agents.judge_agent import JudgeAgent
from pandasai.ee.agents.advanced_security_agent import AdvancedSecurityAgent
from pandasai.ee.vectorstores import ChromaDB
from pandasai.responses.streamlit_response import StreamlitResponse
from pandasai.connectors import PandasConnector
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from PromptRefining import refine_prompt
from file_io import save_to_excel


#---------------------------<><><><><><><><><><><><><><><><>---------------------------
#---------------------------<><><><><><><><><><><><><><><><>---------------------------

env_loaded = load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
api_key_google = os.getenv("GOOGLE_API_KEY")
os.environ["PANDASAI_API_KEY"] = os.getenv("PANDASAI_API_KEY")


llm_llama = ChatGroq(
    model_name="llama-3.1-70b-versatile",  # **1
    api_key = api_key)

# llm_llama = ChatGroq(
#     model_name="gemma2-9b-it", 
#     api_key = api_key,
#     temperature=0)

# llm_llama = ChatGroq(
#     model_name="llama-3.1-8b-instant", 
#     api_key = api_key)

# Instantiate the vector store
vector_store = ChromaDB()
#---------------------------<><><><><><><><><><><><><><><><>---------------------------
#---------------------------<><><><><><><><><><><><><><><><>---------------------------

file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "XLSX": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
}
field_descriptions = {
    'Transaction ID'    :   'A unique identifier for each transaction, allowing tracking and reference.',
    'Date'              :   'The date when the transaction occurred, providing insights into sales trends over time.',
    'Customer ID'       :   'A unique identifier for each customer, enabling customer-centric analysis.',
    'Gender'            :   'The gender of the customer (Male/Female), offering insights into gender-based purchasing patterns.',
    'Age'               :   'The age of the customer, facilitating segmentation and exploration of age-related influences.',
    'Product Category'  :   'The category of the purchased product (e.g., Electronics, Clothing, Beauty), helping understand product preferences.',
    'Quantity'          :   'The number of units of the product purchased, contributing to insights on purchase volumes.',
    'Price per Unit'    :   'The price of one unit of the product, aiding in calculations related to total spending.',
    'Total Amount'      :   'The total monetary value of the transaction, showcasing the financial impact of each purchase.'
    }
Description = """This is the Retail Sales and Customer Demographics Dataset, capturing essential attributes that drive retail operations and customer interactions. It includes key details such as Transaction ID, Date, Customer ID, Gender, Age, Product Category, Quantity, Price per Unit, and Total Amount. These attributes enable a multifaceted exploration of sales trends, demographic influences, and purchasing behaviors."""

Queries = ["""I need the unique Product Categories along with their month-wise and gender-wise total Quantity and Total Amount presented in a table format for the year 2023. The table should be structured with the following specifications:
- Filter the data based on the 'Date' column to include only records within the year 2023.
- Format the month names as 'Jan', 'Feb', 'Mar', etc., in chronological order.
- Ensure the table clearly labels all rows and columns, including 'Product Category' for the index column and 'Month' and 'Gender' for the columns.
- Add a grand total row at the end of the table with the name of 'Grand Total' showing the summed values for Quantity' and 'Total Amount' across all months.
- Ensure the data is presented in a pivot table format, with 'Quantity' and 'Total Amount' as multi-level column headers, and output it as a well-structured Pandas DataFrame.
""",
"""Plot a bar chart to visualize month-wise total Quantity for each gender (Male and Female) and Product Category for the year 2023. The chart should follow these specifications:
- X-axis will display month names in chronological order: Jan, Feb, Mar, etc.
- Each bar will represent the total Quantity for a specific month, divided into segments by Product Category and gender.
- Include a legend for both gender and product category, with clear formatting and a title.
- Show the value on each bar segment in the chart.
- Use distinct, standard colors for each product category within each gender.
- Include an appropriate chart title and titles for both the X-axis and Y-axis.
- Clearly label the X-axis and Y-axis values.
- Adjust the chart's width and height for readability, ensuring all values are visible without overlap. 
"""
]
Responses = ["""      
import pandas as pd

# Create DataFrame
df = pd.DataFrame(dataset)
# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Filter data for the year 2023
df_2023 = df.loc[df['Date'].dt.year == 2023].copy()

# Extract month names
df_2023.loc[:, 'Month'] = df_2023['Date'].dt.strftime('%b')

# Group by Product Categories, Month, and Gender and calculate total Quantity and Total Amount
grouped = df_2023.groupby(['Product Category', 'Month', 'Gender']).agg({'Quantity': 'sum', 'Total Amount': 'sum'}).reset_index()

# Pivot the table
pivot_table = grouped.pivot_table(index='Product Category', columns=['Month', 'Gender'], values=['Quantity', 'Total Amount'], fill_value=0)

# Sort columns by month order
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
pivot_table = pivot_table.reindex(month_order, axis=1, level=1)

# Add grand total for each month and for the entire year
pivot_table[('Grand Total', '', '')] = pivot_table.sum(axis=1)
grand_total = pivot_table.sum(axis=0).to_frame().T
grand_total.index = ['Grand Total']
grand_total.columns = pd.MultiIndex.from_tuples(grand_total.columns)
pivot_table = pd.concat([pivot_table, grand_total], axis=0)
pivot_table
""",
""" 
import pandas as pd
import matplotlib.pyplot as plt
import calendar
# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Filter data for the year 2023
df = df[df['Date'].dt.year == 2023]

# Extract month name from Date column
df['Month'] = df['Date'].dt.month_name().str[:3]

# Group by Month, Gender, and Product Category and sum the Quantity
grouped_df = df.groupby(['Month', 'Gender', 'Product Category'])['Quantity'].sum().unstack().unstack()

# Reindex to ensure all months are present in chronological order
grouped_df = grouped_df.reindex(calendar.month_abbr[1:], axis=0)

# Plotting
fig, ax = plt.subplots(figsize=(15, 10))
grouped_df.plot(kind='bar', stacked=True, ax=ax)

# Adding values on top of bars
for container in ax.containers:
    ax.bar_label(container, label_type='center')

# Setting labels and title
ax.set_xlabel('Month')
ax.set_ylabel('Total Quantity')
ax.set_title('Month-wise Total Quantity by Gender and Product Category for the Year 2023')
ax.legend(title='Gender and Product Category')

# Display the plot
plt.show()
"""]
Docs = """
- To ensure secure execution, the code should avoid using functions such as 'os', 'io', 'chr', or 'b64decode'. 
- A value is trying to be set on a copy of a slice from a DataFrame. Try using .loc[row_indexer,col_indexer] = value instead
"""


#---------------------------<><><><><><><><><><><><><><><><>---------------------------
#------------------------------------Define Function-----------------------------------
def load_data(uploaded_file):
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except:
        ext = uploaded_file.split(".")[-1]
    if ext in file_formats:
        return file_formats[ext](uploaded_file)
    else:
        # st.error(f"Unsupported file format: {ext}")
        return None
    
def chat_with_data(df,prompt,folder):
    head_df = df.sample(10) 
    connector = PandasConnector({"original_df": df}, field_descriptions=field_descriptions)
    sdf = SmartDataframe(connector, name="ArTraderAnalysis", description= Description,config={'llm': llm_llama})
    judge = JudgeAgent()
    security = AdvancedSecurityAgent()
    pandas_ai_agent = Agent(sdf,config={'llm': llm_llama,
                                    "save_logs": True,
                                    "save_charts" : True,
                                    "save_charts_path": f"exports/{folder}/",
                                    "enforce_privacy":True,
                                    "enable_cache" : True,
                                    "custom_head": head_df,
                                    "use_error_correction_framework" : True,
                                    "verbose": True, 
                                    "response_parser": StreamlitResponse,
                                    "custom_whitelisted_dependencies": ["plotly"]
                                    },
                            judge=judge,
                            security=security,
                            vectorstore=vector_store,
                            description="You are a data analysis agent. Your main goal is to help non-technical users to analyze data and give the correct answer of their questions."
                            )
    # pandas_ai_agent.train(queries=Queries,codes= Responses)
    result = pandas_ai_agent.chat(prompt)
    return result
    

#---------------------------<><><><><><><><><><><><><><><><>---------------------------
