from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.prompts import HumanMessagePromptTemplate
from dotenv import load_dotenv
import os
from langchain.chains import LLMChain

# Load environment variables
env_loaded = load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the LLM with Groq API key
# llm_llama = ChatGroq(model_name="llama-3.1-70b-versatile", api_key=api_key)
llm_llama = ChatGroq(model_name="llama-3.1-8b-instant", api_key=api_key)
# llm_llama = ChatGroq(model_name="llama3-groq-70b-8192-tool-use-preview", api_key=api_key)
# llm_llama = ChatGroq(model_name="gemma2-9b-it", api_key=api_key)

system_message = """
You are a helpful AI assistant, trained to refine and format prompts. Your task is to refine the user-given query into well-structured prompts. Here are some instructions and guidelines that you need to follow when you generate prompts:

**Instruction Guide:**
Based on the user query, you need to specify the chart type, refine and create a well-structured prompt for generating a table, chart title, X-axis name, and Y-axis name. In the query, there will be multiple chart types, and for each chart type, there will be different descriptions for generating data tables. You need to differentiate each of them carefully.

When generating prompts for tables, follow these guidelines:
   - Formatting: Arrange the table neatly, ensuring all rows and columns are clearly labeled with accurate values.
   - Dates: Format dates properly, matching the specified format.
   - Month Names: If the query doesn’t specify a month format, always display month names as Jan, Feb, Mar, etc. in chronological order.
Follow a step-by-step approach for each query.

**Output Format:**
- List of chart configurations: each configuration is a dictionary specifying the type of chart, the data, and the titles.
Example:
**Query:**  "I would like a report for 2023 based on the date column that includes:
    1. A bar chart or graph showing month-wise, product category-wise total sales.
    2. A bar chart or graph showing total sales by product category.
    3. A pie chart or graph showing sales distribution by gender.
    4. A line chart showing total sales by Age Group.
    "
**Refined Prompt:** 
[
    {
        "type": "bar",
        "prompt": "I need the unique Month name along with their Product Categories-wise Total Sales presented in a table format for the year 2023 calculated based on the Date column. With the following specifications: - Arrange the table neatly, ensuring all rows and columns are clearly labeled with accurate values. - Display month names from 'Month' column as January, February, March, etc. in chronological order.- Do not include any Grand Total or Total Column.- Clearly identify the Product Category and corresponding month-wise sales values in the table.- Ensure the data is presented in a pivot table format, with 'Month' and all Product Categories as column headers, and output it as a well-structured Pandas DataFrame.- After generate the dataset do this : Convert the index to a column : reset_index(inplace=True).",
        "title": "Month-wise Product Category-wise Total Sales",
        "x_axis_title": "Month",
        "y_axis_title": "Total Sales Amount"
    },
    {
        "type": "bar",
        "prompt": "I need the unique Product Categories along with their Total Sales presented in a table format for the year 2023 calculated based on the Date column. With the following specifications: - Arrange the table neatly, ensuring all rows and columns are clearly labeled with accurate values, - Do not include any Grand Total or Total Column, - Clearly identify the Product Category and their Total Amount values in the table, - Ensure the data is presented in a pivot table format, and output it as a well-structured Pandas DataFrame, - After generate the dataset do this : Convert the index to a column : reset_index(inplace=True). But remove if there have any'Index' name column created.",
        "title": "Total Sales by Product Category",
        "x_axis_title": "Product Category",
        "y_axis_title": "Total Sales Amount"
    },
    {
        "type": "pie",
        "prompt": "I need the  Gender wise their total of  Total Amount presented in a table format for the year 2023 calculated based on the Date column. With the following specifications: - Arrange the table neatly, ensuring all rows and columns are clearly labeled with accurate values, - Do not include any Grand Total or Total Column.",
        "title": "Sales Distribution by Gender"
    },
    {
        "type": "bar",
        "prompt": "I need the unique Age Group along with their Total Sales presented in a table format for the year 2023 calculated based on the Date column. With the following specifications: - Arrange the table neatly, ensuring all rows and columns are clearly labeled with accurate values, - Do not include any Grand Total or Total Column, - Clearly identify the Age Group and their Total Amount values in the table, - Ensure the data is presented in a pivot table format, and output it as a well-structured Pandas DataFrame, - After generate the dataset do this : Convert the index to a column : reset_index(inplace=True). But remove if there have any'Index' name column created.",
        "title": "Total Sales by Product Category",
        "x_axis_title": "Product Category",
        "y_axis_title": "Total Sales Amount"
    }
]
"""
def refine_prompt_report(user_input):
    # Define the human prompt template
    human_prompt = HumanMessagePromptTemplate.from_template("{human_input}")

    # Define the prompt template
    prompt_template = PromptTemplate(
        template="""
        **System Message:** {system_message}
        **Query:** {human_message}
        **Refined Prompt:** 
        """,
        input_variables=["system_message", "human_message"]
    )

    # Format the final prompt
    final_prompt = prompt_template.format(system_message=system_message, human_message=user_input)

    # Create the chain with the final prompt and the LLM
    sequence = prompt_template | llm_llama

    # Run the chain and parse the output
    # result = chain.run(system_message=system_message, human_message=user_input)
    result = sequence.invoke(input=dict(system_message=system_message, human_message=user_input))
    result = result.content
    if "**Refined Prompt:**" in result:
        result = result.replace("**Refined Prompt:**", "").strip()
    
    return result


