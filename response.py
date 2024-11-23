import pandas as pd
import json
from chatbot import load_data
from chatbot import chat_with_data
from PromptRefining import refine_prompt
from PromptRefining_report import refine_prompt_report
from report import create_report
from file_io import save_to_excel

uploaded_file = 'retail_sales_dataset.csv'
dataset = load_data(uploaded_file)
dataset["Date"] = pd.to_datetime(dataset["Date"], errors="coerce")
dataset['Month'] = dataset['Date'].dt.strftime('%B')
dataset['Age Group'] = pd.cut(dataset['Age'], bins=[0, 20, 30, 40, 50, 60, 70], labels=['<20', '20-29', '30-39', '40-49', '50-59', '60+'])
# print(dataset)

# query = """Report : I would like a report for 2023 based on the date column that includes:
#     1. A bar chart showing month-wise, product category-wise total sales.
#     2. A pie chart showing total sales by gender.
#     3. A pie chart showing total Sales by Product Category.
#     4. A line chart showing total sales by Age Group.
#     """
    
query = "Plot an bar chart of month-wise total Quantity for each gender  and Product Category for the year 2023 based on the Date column"


# query = input("Enter your query: ")
folder = "ashish"
# refine_query = refine_prompt(query)
# print(refine_query)

# Trigger Function get reponse from data-set
def get_final_response(query):
    if "Excel :" in query:
        query = query.replace("Excel :", "").strip()
        refine_query = refine_prompt(query)
        answer = chat_with_data(dataset,refine_query,folder)
        file_link = save_to_excel(answer,folder)
        print(file_link)
        return file_link
    elif "Report :" in query:
        query = query.replace("Report :", "").strip()
        # print(query)
        refine_query_report = refine_prompt_report(query)
        # print(type(refine_query_report))
        refined_prompt_list = json.loads(refine_query_report)
        # print(type(refined_prompt_list))
        # print(refined_prompt_list)
        report_link = create_report(dataset, refined_prompt_list, folder)
        print(report_link)
        return report_link
        
    else:
        refine_query = refine_prompt(query)
        answer = chat_with_data(dataset,refine_query,folder)
        print(answer)
        return answer
    


# Slack Bot 
