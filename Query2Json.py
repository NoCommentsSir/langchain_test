from libs import *

chat = GigaChat(credentials=os.environ["GIGACHAT_CREDENTIALS"],verify_ssl_certs=False,scope="GIGACHAT_API_PERS")

class Agent:
  query = ""
  class Format(BaseModel):
    pass

  def __init__(self, query, Format):
    self.query = query
    self.Format = Format

  def talk(self):
    parser = PydanticOutputParser(pydantic_object=self.Format)
    prompt = PromptTemplate(
      template="You should find and extract the object and its properties. Then you should make json file of this object and its attributes. Talk in Englis.\n{format_instructions}\n{query}\n",
      input_variables=["query"],
      partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | chat | parser
    ans = chain.invoke({"query": self.query})
    return ans

query = input()
class Film(BaseModel):
  name: str
  author: str
  country: str

AI = Agent(query, Film)
ans = AI.talk()
print(ans)