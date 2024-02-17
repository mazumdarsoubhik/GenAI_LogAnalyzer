import streamlit as st
import pandas as pd
import time

st.title("Prod Incident Cause Analysis Using GenAI 🧠")
st.write("---")

st.title(":blue[Initiate Analysis Request] :warning:")

col1, col2 = st.columns(2)

## Increase the size of the labels
with col1:
    st.write('Select your LLM')
    title = st.text_input('Blocked for now', 'Antrhopic', disabled=True)
with col2:
    st.write('Select your App Framework')
    option = st.selectbox(
        "Choose from dropdown",
        ("Dot Net", "IBM BPM", "Linux"),
    )
## Increase the size of the labels
workaround = st.text_area(
    "# Instructions or Workaround (Optional)",
    # "It was the best of times, it was the worst of times, it was the age of ",
    )
st.write(f'You wrote {len(workaround)} characters.')


########## UPOLOAD FILE
uploaded_file = st.file_uploader(  "Upload your log file", 
                                    accept_multiple_files=False,
                                    type=['txt'],
                                    )
if uploaded_file is not None:
    print(type(uploaded_file))
    with open('input/user_input.txt', 'wb') as file:
        file.write(uploaded_file.read())
    
    with open('input/user_input.txt', 'r') as file:
        st.text_area('Input Log File', ''.join(file), height=400)

        
if st.button("Generate Analysis :mag:", type="primary"):
    progress_text = "Initiating server..."
    my_bar = st.progress(0, text=progress_text)
    time.sleep(1)
    
    ########## Backend - Chunking
    progress_text = "Chunking log file..."
    my_bar.progress(20, text=progress_text)

    ######### Backend - VectorDB
    progress_text = "Initiaing VectorDB and Inserting vectors..."
    my_bar.progress(30, text=progress_text)
    
    ######### Backend - LLM
    progress_text = "Initiaing LLM API..."
    my_bar.progress(50, text=progress_text)
    
    ######### Backend - Chunk Summaries
    progress_text = "Summerizing chunks..."
    my_bar.progress(70, text=progress_text)
    
    ######## Backend - Report Generation
    progress_text = "Generating report..."
    my_bar.progress(80, text=progress_text)
    
    ######## Printing the report
    progress_text = "Publishing the report..."
    my_bar.progress(100, text=progress_text)
    time.sleep(2)
    
    my_bar.empty()
    
    report={'Cause': 'The incidents were caused by:\n\n- Missing view file resulting in ViewNotFoundException\n- Invalid file path leading to FileNotFoundException \n- Database connectivity issues causing SqlException\n- Attempt to divide by zero resulting in DivideByZeroException\n- Potential null reference or divide by zero in StatsService', 'Solution': 'Some solutions to fix these are:\n\n- For missing view, ensure view file exists in expected location\n- Validate file path before processing file import\n- Check database connection string, network connectivity\n- Add null check before division to prevent divide by zero\n- Validate input arrays to avoid null reference\n- Add detailed exception handling and logging\n- Handle expected exceptions like FileNotFound and DivideByZero specifically\n- Review calculation logic to prevent errors\n- Add more logging at exception origin to identify root cause'}
    
    ####### Display Report
    st.title(":blue[Incident Analysis Report] :zap:")
    
    tab1, tab2, tab3 = st.tabs(["Analysis", "Solution", "References"])

    with tab1:
        st.header("Incident Cause Analysis")
        md = st.text_area('Below is the cause report generated', report['Cause'], height=400)
    
    with tab2:
        st.header("Suggested Solution")
        md = st.text_area('Below is the solution report generated', report['Solution'], height=400)
    
    with tab3:
        with open('output/interim_output.txt', 'r') as ref_file:
            st.header("Chunk Summaries Used for Report")
            md = st.text_area('Below are the references utilized', ''.join(ref_file), height=400)
    
    ####### Save Report
    with open('output/final_report.txt', 'w') as final_report:
        final_report.write('---------------- CAUSE ANALYSIS ----------------\n')
        final_report.write(report['Cause'])
        final_report.write('\n\n---------------- SUGGESTED SOLUTION ----------------\n')
        final_report.write(report['Solution'])
        final_report.write('\n\n---------------- REFERENCES ----------------\n')
        with open('output/interim_output.txt', 'r') as ref:
            final_report.write(''.join(ref))
            
    st.download_button("Download Report", open('output/final_report.txt'))
    
