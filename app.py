import streamlit as st
import pandas as pd
import time, math
import logging, os, time
from datetime import datetime
import Chunking, VectorDB, LLM, SmallSummary, LargeSummary

######## Initiate Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"syslogs/{__name__}.log")
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

logger.info("Staring up...\n")

st.title("Prod Incident Cause Analysis Using GenAI 🧠")
st.write("---")

st.title(":blue[Initiate Analysis Request] :warning:")

col1, col2 = st.columns(2)
with col1:
    st.write('Select your LLM')
    title = st.text_input('Blocked for now', 'Anthropic', disabled=True)
with col2:
    st.write('Select your App Framework')
    option = st.selectbox(
        "Choose from dropdown",
        ("Dot Net", "IBM BPM", "Linux"),
    )
    frameworks={
        'Dot Net':'dotnet',
        'IBM BPM':'ibmbpm',
        'Linux':'linux'
    }
    

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
    
    start_time = time.time()
    
    progress_text = "Initiating server..."
    my_bar = st.progress(0, text=progress_text)
    time.sleep(1)
    
    ########## Backend - Chunking
    progress_text = "Chunking log file..."
    my_bar.progress(20, text=progress_text)
    chunking_obj = Chunking.LineBasedChunk("dotnet.txt")
    all_chunks = chunking_obj.getChunks()

    ######### Backend - VectorDB
    progress_text = "Initiaing VectorDB and Inserting vectors..."
    my_bar.progress(30, text=progress_text)
    vectorDB_obj = VectorDB.FAISS_VDB('dotnet')
    vectorDB = vectorDB_obj.getVectorDB()
    
    ######### Backend - LLM
    progress_text = "Initiaing LLM API..."
    my_bar.progress(50, text=progress_text)
    llm_obj = LLM.Anthropic()
    llm_small = llm_obj.get('light', 500)
    llm_large = llm_obj.get('heavy', 20000)
    
    # ######### Backend - Chunk Summaries
    progress_text = "Summerizing chunks..."
    my_bar.progress(70, text=progress_text)
    chunk_summary_obj = SmallSummary.ChunkSummaries()
    fileOfSummaries = chunk_summary_obj.getSummeries(all_chunks, llm_small, vectorDB, workaround, frameworks[option])
    
    ######## Backend - Report Generation
    progress_text = "Generating report..."
    my_bar.progress(80, text=progress_text)
    report_generation_obj = LargeSummary.GenerateReport()
    total_trial=5
    while total_trial > 0:
        try:
            report=report_generation_obj.getSummary(fileOfSummaries, llm_large)
            break
        except Exception as e:
            print("Failed report generation", e)
            total_trial -= 1  
            
    ######## Printing the report
    progress_text = "Publishing the report..."
    my_bar.progress(100, text=progress_text)
    time.sleep(2)
    
    my_bar.empty()
    
    # report={'Cause': 'The incidents were caused by:\n\n- Missing view file resulting in ViewNotFoundException\n- Invalid file path leading to FileNotFoundException \n- Database connectivity issues causing SqlException\n- Attempt to divide by zero resulting in DivideByZeroException\n- Potential null reference or divide by zero in StatsService', 'Solution': 'Some solutions to fix these are:\n\n- For missing view, ensure view file exists in expected location\n- Validate file path before processing file import\n- Check database connection string, network connectivity\n- Add null check before division to prevent divide by zero\n- Validate input arrays to avoid null reference\n- Add detailed exception handling and logging\n- Handle expected exceptions like FileNotFound and DivideByZero specifically\n- Review calculation logic to prevent errors\n- Add more logging at exception origin to identify root cause'}
    
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
    
    end_time = time.time()
    
    st.download_button("Download Report", open('output/final_report.txt'))
    
    
    ####### Calculate Impact
    with open('output/interim_output.txt', 'r') as ref_file:
        token_count = 0
        file_size = 0
        for line in ref_file:
            token_count += 2 * llm_large.get_num_tokens(line)
            file_size += 1
        print(file_size, token_count)
        st.write(f"""
        ## :blue[Impact] 🚀
        - Time taken by *GenAI* method: **{math.ceil((end_time-start_time)/60)} mins**
        - Cost incurred by *GenAI* method: **${round((token_count//1000)*0.024*2, 4)}**
        - It would have taken **{file_size//120} hours** and costed **${(file_size//120)*30}** to analyze it manually.
        """)



