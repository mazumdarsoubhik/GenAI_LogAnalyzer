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

########## Chunking
chunking_obj = Chunking.LineBasedChunk("dotnet.txt")
all_chunks = chunking_obj.getChunks()

######### VectorDB
vectorDB_obj = VectorDB.FAISS_VDB('dotnet')
vectorDB = vectorDB_obj.getVectorDB()

######### LLM
llm_obj = LLM.Anthropic()
llm_small = llm_obj.get('light', 500)
llm_large = llm_obj.get('heavy', 20000)

######### Chunk Summaries
workaround="No Workaround"
framework='dotnet'
chunk_summary_obj = SmallSummary.ChunkSummaries()
fileOfSummaries = chunk_summary_obj.getSummeries(all_chunks, llm_small, vectorDB, workaround, framework)

######## Report Generation
report_generation_obj = LargeSummary.GenerateReport()

total_trial=5
while total_trial > 0:
    try:
        report=report_generation_obj.getSummary(fileOfSummaries, llm_large)
        break
    except Exception as e:
        print("Failed report generation", e)
        total_trial -= 1

print(report)
