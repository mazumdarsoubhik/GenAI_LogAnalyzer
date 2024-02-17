from abc import ABC, abstractmethod
from IPython.display import display, clear_output
import time, os

class SmallSummary(ABC):
    @abstractmethod
    def getSummeries(self, chunks: list, llm: object, vectorStore: object) -> str:
        """
        Used to answer queries of total token less then max token of LLM. 
        Each chunk will contain the query, it'll be wrapped in prompt with context to get accurate answers.
        
        Parameters
        llm: LLM API object
        vectorStore: VectorDB object for similarity search
        
        Returns
        Path to the file which contains answer for all the chunks.
        """
        pass
    
    @abstractmethod
    def makePrompt(self) -> object:
        """
        Generate the prompt with context, question and kwargs as input variable.
        """
        pass
    
class ChunkSummaries(SmallSummary):
    def getSummeries(self, chunks: list, llm: object, vectorStore: object, workaround: str, framework: str) -> list[str]:
        from langchain.chains import RetrievalQA
        
        
        master_start_time=time.time()
        
        PROMPT=self.makePrompt(workaround, framework)
        
        qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorStore.as_retriever(
            search_type="similarity", search_kwargs={"k": 3}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
        )

        interim_op = f'output/interim_output.txt'
        interim_op_buffer = open(interim_op, "w")

        total_chunks=len(chunks)
        print(f'Total chunks to summerize: {total_chunks}')
        i=0
        display(f'{i}/{total_chunks} chunks summerized...')
        for chunk in chunks:
            start_time=time.time()
            results = qa({"query": chunk})
            chunk_summary = f"\n*------*Query*------*\n{results['query']}\n\n*------*Answer*------*\n{results['result']}\n==========\n"
            interim_op_buffer.write(chunk_summary)
            end_time=time.time()
            i+=1
            clear_output(wait=True)
            display(f'{i}/{total_chunks} chunks summerized completed... ({round(end_time-start_time,2)} secs)')

        interim_op_buffer.close()
        master_end_time=time.time()
        print(f'==== END OF SUMMERIZING CHUNKS {round(master_end_time-master_start_time, 2)} secs=====\n')
        return interim_op

    def makePrompt(self, workaround: str, framework: str) -> object:
        from langchain.prompts import PromptTemplate

        prompt_template=[
        """
        Human: You are a server or application log analysis LLM which provides accurate output without hallucination. You will be given a small chunk of a large log file and you need to analyze (If Error or Failure) and tell the problem (along with actual cause) and suggest solution to fix it as an output. It the chunk is just INFO then summarize it in a few lines as output.
        """,
        f'The server or application framework is: {framework}',
        """
        To complete the task you'll be given 'Question' which contains the log chunk, 'Context' which may support you on analyzing the chunk and 'Workaround' which may give you background on the analysis done by other teams. Consider all this to reach to an accurate output.

        <Question>
        {question}
        </Question>

        <Context>
        {context}
        </Context>
        """,
        f'\n<Workaround>\n{workaround}\n</Workaround>',
        """
        Assistant:
        """]
        
        PROMPT = PromptTemplate(template=''.join(prompt_template),
                                input_variables=['question', 'context']
                               )
        return PROMPT
    
    