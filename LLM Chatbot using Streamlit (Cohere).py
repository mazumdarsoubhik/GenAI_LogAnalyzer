#### How to Run ####
# 1. pip install streamlit
# 2. pip install cohere
# 3. Copy your API key to `MY_API_KEY`
# 4. Put your prompts in `system_prompt` and `filter_prompt`
# 5. Execute `streamlit run 'LLM Chatbot using Streamlit.py'`
# 6. Use external IP on browser to chat.
####################

import streamlit as st
from streamlit_chat import message
import random, time, string
import time

MY_API_KEY="<Your Own API Key" # Put your cohere API key. For key log in to https://dashboard.cohere.com/api-keys

class CohereLLMAPI:
    _name="Cohere"
    _models=["command", "command-r-plus"]
    _model=None
    _API_KEY=None
    _instance=None
    _chat_id=None
    _system_prompt=None
    _filter_prompt=None
    
    def __init__(self, KEY: str, system_prompt: str, filter_prompt: str, model="command-r-plus"):
        import cohere
        self._API_KEY=KEY
        self._system_prompt=system_prompt
        self._filter_prompt=filter_prompt
        try:
            # Validate and fixate LLM model
            if model not in self._models: # If model belongs to Cohere list
                raise ValueError(f"\n\tInvalid LLM model: {model}")
            self._model=model
            
            # Generate Chat ID - Randomised
            self._chat_id = ''.join(random.choices(string.ascii_letters, k=10))
            
            # Initiate API
            self._instance=cohere.Client(api_key=self._API_KEY)
            
            # Specify behaviour: Set system prompt to LLM
            stream = self._instance.chat_stream(
            message=self._system_prompt,
            conversation_id=self._chat_id
            )
            
        except Exception as e:
            print(f"Failed connecting to {self._name} API: {e}")
    
    def change_key(self, new_KEY):
        self._API_KEY=new_KEY
        self._instance=cohere.Client(api_key=self._API_KEY)
    
    def text_generate(self, input_text):
        return co.chat(
            message=input_text,
            model=self._model).text
    
    def chat_stream_print(self, user_message):
        stream = self._instance.chat_stream(
            message=self._filter_prompt + f"\nUser:\n" + user_message,
            conversation_id=self._chat_id
        )

        for event in stream:
            if event.event_type == "text-generation":
                print(event.text, end='')
    
    def yield_reponse(self, user_message):
        stream = self._instance.chat_stream(
            message=self._filter_prompt + f"\nUser:\n" + user_message,
            conversation_id=self._chat_id
        )
        
        for event in stream:
            if event.event_type == "text-generation":
                yield event.text + ""
                time.sleep(0.05)


#### ChatBot Prompt ####

system_prompt="""
You are Aime, a knowledgeable virtual assistant specializing in Australian policy regulations. Your primary focus is to provide accurate and up-to-date information on regulations from the Australian Prudential Regulation Authority (APRA) and other relevant regulatory bodies.

When users ask about Australian policy regulations, such as APRA guidelines, regulatory updates, or compliance requirements, respond with clear, concise information and guidance. Provide insights into regulatory processes, recent changes, and how they impact various sectors.

For example:
- If a user asks about recent APRA guidelines, provide a summary of the latest guidelines, their purpose, and their implications for businesses.
- If a user inquires about compliance requirements, detail the necessary steps or documentation needed to comply with APRA regulations.

Remember, your responses should be informative, accurate, and relevant to Australian regulatory policies.

Briefly introduce yourself and provide a bullet-point list of your capabilities.
"""
filter_prompt="""
Instruction for Responses:
- Focus exclusively on policies: Your responses should be limited to providing information about Australian policies, regulations, and related guidelines.
- No unrelated information: Do not answer questions or provide information about topics that are not directly related to policies, regulations, or compliance issues. This includes general knowledge, personal opinions, or unrelated technical or non-policy-related topics.
- Clarify when uncertain: If a query does not pertain to policy-related matters, politely inform the user that your expertise is focused on policies and suggest that they ask a question related to that domain.
"""

#########################

# Initiating the LLM
llm_api = CohereLLMAPI(MY_API_KEY, system_prompt, filter_prompt) # Initiate with API Key


# The Streamlit App
st.title("APRA Guideline Chatbot")
 
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
 
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
 
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(llm_api.yield_reponse(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
 