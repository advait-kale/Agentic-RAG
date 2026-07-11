from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from app.config.settings import Settings

settings = Settings()

llm_model = settings.llm_model
llm_provider = settings.llm_provider
llm_temperature = 0.0


class ChatService:
    def __init__(self):
        self.llm = init_chat_model(
            model=llm_model,
            model_provider=llm_provider,
            temperature = llm_temperature,
            reasoning=False
            # max_tokens = 
            # timeout = 
        )
    async def generate_answer(self, query: str, context):
        RAG_Prompt = """
        Use the given Context give an answer to the query
        <context>
        {context}
        </context>

        <query>
        {query}
        </query>

        Answer: 
        """

        System_Prompt = """You are a helpful AI assistant for customer support that answers questions based on provided context.

                            IMPORTANT RULES:
                            1. For questions about policies, returns, shipping, sizing, or support: Answer ONLY using the provided context and include citations
                            2. For general greetings or casual conversation: You can respond naturally and friendly
                            3. For questions outside your knowledge base: Politely redirect to relevant policies or suggest contacting support
                            4. Be concise but comprehensive
                            5. Maintain a helpful, professional tone"""
        
        RAG_Prompt = RAG_Prompt.format(context= context, query = query)
        
        messages=[
            SystemMessage(System_Prompt),
            HumanMessage(RAG_Prompt),
                ]

        buffer = ""
        passed_think = False
        started = False        
        for ans in self.llm.stream(messages):
            token = ans.content or ""
            if passed_think:
                if not started:
                    token = token.lstrip()
                    if not token:
                        continue
                    started = True
                yield token
                continue
            buffer += token
            if "</think>" in buffer:
                passed_think = True
                after = buffer.split("</think>", 1)[1].lstrip()
                buffer = ""
                if after:
                    started = True
                    yield after

        if not passed_think and buffer:
            yield buffer.lstrip()


chat = ChatService()
    
    