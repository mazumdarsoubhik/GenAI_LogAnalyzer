## Execute them manually from terminal

!pip install --no-build-isolation --force-reinstall \
    "boto3>=1.28.57" \
    "awscli>=1.29.57" \
    "botocore>=1.31.57"
    
!pip install --quiet \
    langchain==0.0.309 \
    "transformers>=4.24,<5" \
    sqlalchemy -U \
    "faiss-cpu>=1.7,<2" \
    "pypdf>=3.8,<4" \
    pinecone-client \
    apache-beam \
    datasets \
    tiktoken \
    "ipywidgets>=7,<8" \
    matplotlib
    
!pip install --quiet \
    xmltodict==0.13.0  \
    duckduckgo-search  \
    yfinance  \
    pandas_datareader  \
    langchain_experimental \
    pysqlite3 \
    google-search-results
    
!pip install --quiet beautifulsoup4

!pip install --quiet "pillow>=9.5,<10"

%%bash
apt-get update && apt-get install g++ -y

!pip install -qU --no-cache-dir nemoguardrails==0.5.0

!pip install -qU "faiss-cpu>=1.7,<2" \
                      "langchain==0.0.309" \
                      "pypdf>=3.8,<4" \
                      "ipywidgets>=7,<8"
