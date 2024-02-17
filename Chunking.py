from abc import ABC, abstractmethod

class Chunking(ABC):
    @abstractmethod
    def getChunks(self, file_name: str) -> list[str]:
        """
        Chunks the file given in the input/file_name by certain amount of line. A particular chunk may contain a few lines from the file.
        file_name : str
        
        return an list of chunks.
        """
        pass

class LineBasedChunk(Chunking):
    def __init__(self, file_name):
        self.path=f'input/{file_name}'
        
    def getChunks(self):
        print(f'\n===== CHUNKING LOG FILE =====\n')
        lines_per_chunk = 10
        all_chunks = []

        with open(self.path) as bigfile:
            chunk=""
            for lineno, line in enumerate(bigfile):
                if (lineno+1) % lines_per_chunk == 0:
                    all_chunks.append(chunk)
                    chunk=""
                chunk += '\n' + line

            all_chunks.append(chunk)

        print(f'Total {len(all_chunks)} chunks extracted.\n===== END OF LOG CHUNKING =====\n')
        return all_chunks  
    
class ErrorBasedChunk(Chunking):
    def getChunks(self, file_name):
        pass