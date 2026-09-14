from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3-0324",
    huggingfacehub_api_token=None
)

model = ChatHuggingFace(llm=llm)

response = model.invoke("who is lana rhodes?")
print(response.content)