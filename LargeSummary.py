from abc import ABC, abstractmethod

class LargeSummary(ABC):
    @abstractmethod
    def getSummary(self, path: str, llm: object) -> dict:
        pass

class GenerateReport(LargeSummary):
    def getSummary(self, path, llm):
        from langchain.chains.summarize import load_summarize_chain
        from langchain.prompts import PromptTemplate
        from langchain.output_parsers import XMLOutputParser, PydanticOutputParser
        from langchain.output_parsers.json import SimpleJsonOutputParser
        from langchain.schema.output_parser import StrOutputParser
        import json
        
        ######### List down chunk summaries
        docs=[]
        with open(path, "r") as file:
            chunk=""
            for line in file:
                # print(line)
                if '===' in line[:3]:
                    docs.append(chunk)
                    chunk=""
                elif line.strip() == '':
                    continue
                else:
                    chunk += line + '\n'
            docs.append(chunk)

        str_parser = StrOutputParser()

        prompt = PromptTemplate(
            template="""

            Human:
            {instructions} : \"{document}\"
            Assistant:""",
            input_variables=["instructions","document"]
        )

        summary_chain = prompt | llm | StrOutputParser()
        
        instruction_prompt="""
You'll be provided multiple sets of log analysis insights. In each insights there is a problem and it's analysis. The problem will be given under *------*Query*------* and the analysis will be given under *------*Answer*------*. 
Compile and summarize these insights into a JSON and provide (1) the Cause of Incident (2) the Possible solutions to fix the incident.
Explain in detail what was the cause of incident with technical accuracy, you may use bullet points too. 
Give the possible solution in detail considering it'll be read by a fresher who need each and every step in technical details.
Generate these in markdown language.
The ouput MUST ONLY be a JSON which contains 'Cause' and 'Solution' as the only key.
Example Ouput Format: {'Cause': <Cause of Incident>, 'Solution': <Possible solutions to fix the incident>}
        """
        
        # print("The large summary prompt:", instruction_prompt)
        
        ######## Execute summarization
        report=summary_chain.invoke({
                "instructions":instruction_prompt,
                "document": {'\n'.join(docs)}
            })
        
        ######## Extract only JSON
        filter_report=""
        flag=False
        for x in report:
            if x == '{':
                flag=True
            if x == '}':
                filter_report += '}'
                flag=False
            if flag:
                filter_report += x

        filter_report=json.loads(filter_report)
        
        return filter_report
