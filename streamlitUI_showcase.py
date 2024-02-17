import streamlit as st
import pandas as pd
import time
 
st.write("""
# Project Heading
---
## Input Layer (Put Your Query)
""")

col1, col2 = st.columns(2)

## Increase the size of the labels
with col1:
    title = st.text_input('Select your LLM', 'Antrhopic', disabled=True)
with col2:
    option = st.selectbox(
        "Select Application or Server Framework",
        ("Dot Net", "IBM BPM", "Linux"),
    )
## Increase the size of the labels
workaround = st.text_area(
    "# Additional Instructions or Workaround (Optional)",
    # "It was the best of times, it was the worst of times, it was the age of "
    # "wisdom, it was the age of foolishness, it was the epoch of belief, it "
    # "was the epoch of incredulity, it was the season of Light, it was the "
    # "season of Darkness, it was the spring of hope, it was the winter of "
    # "despair, (...)",
    )
st.write(f'You wrote {len(workaround)} characters.')


## Use this for upload file
# uploaded_files = st.file_uploader("Upload your log file", accept_multiple_files=False)
# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)
#     st.write(bytes_data)


# Make it bigger and BOLD, change color to #3239BE4
st.button("Generate", type="primary")

# PROGRESS BAR == Update with display comments
progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

st.button("Rerun")

st.write("""
---
""")

st.write("""
## Output Layer (Results/ My Observations)
""")

tab1, tab2, tab3 = st.tabs(["Cause Analysis", "Suggested Solution", "References"])

# Add text boxes
with tab1:
   st.header("A cat")
   sample = [str(i)+'\n' for i in range(100)]
   md = st.text_area('Below is the cause report generated', ''.join(sample), height=400)

with tab2:
   sample = [str(i)+'\n' for i in range(100)]
   md = st.text_area('Below is the solution report generated', ''.join(sample), height=400)

with tab3:
   sample = [str(i)+'\n' for i in range(100)]
   md = st.text_area('Below are the reference', ''.join(sample), height=400)

## Include icon
st.button("Download Report")


st.write("""
## Impact
- LLM Time taken
- LLM Cost
- Total time saved
- Total cost saved
""")