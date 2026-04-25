import uuid 

from langgraph.func import entrypoint, task 
from langgraph.checkpoint.memory import InMemorySaver 



@entrypoint()
def workflow(inputs: dict) -> str:
    pass 



if __name__ == "__main__":
    pass