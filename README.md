# GenAI_LogAnalyzer
The Generative AI-powered Log Analyzer accelerates production incident debugging for support developers by swiftly analyzing raw log files, providing comprehensive root cause analysis, and suggesting effective remediation strategies. Its versatility makes it a natural fit within the IT support workflow of any organization. Additionally, it seamlessly integrates with popular IT operations management tools such as ServiceNow, serving as a powerful plugin to enhance incident resolution efficiency. With an estimated efficacy of **95% cost reduction** and **90% time reduction** in IT incident resolution, its impact is significant.

## Prerequisites

**Cloud Services:** AWS Bedrock or AWS Sagemaker and AWS Cloud9

**Interpreter:** Python3

**Libraries:** boto3, LangChain, Streamlit

## Steps to Run

1. Clone the repository: `git clone https://github.com/mazumdarsoubhik/GenAI_LogAnalyzer.git`'
2. Go to the directory: `cd GenAI_LogAnalyzer`
3. Create a new virtual environment, activate and install required libraries:
   
   a. `python -m venv venv`
   
   b. `source venv/bin/activate`
   
   c. `pip install -r requirements.txt`
5. Installing AWS prerequisites: `python OneTimeExecution.py`
6. Initiate the app: `streamlit run streamlitUI.py`

## Landing Page
![image](https://github.com/mazumdarsoubhik/GenAI_LogAnalyzer/assets/44722027/4ba19e27-fe09-4490-87eb-d0b0cf2252b5)
