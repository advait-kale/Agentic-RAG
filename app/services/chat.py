from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage, AIMessage
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
        Use the given Context give an answer to the query.
        Name of the sender and due date if available if not don't mention it.
        Any links present should be at the end of the message 
        
        <context>
        {context}
        </context>

        <query>
        {query}
        </query>

        Answer: 
        """

        college_context = """VIT terms
            1. CAT-1 exam, CAT-2 open notes (Hand written), FAT final exam
            2. DA digital assignment
            3. College events dates
            4. Emails from teaher reguarding DA (Digital assignment)
        """

        System_Prompt = """You are a helpful AI assistant for customer support that answers questions based on provided context.

                            IMPORTANT RULES:
                            1. For questions about policies, returns, shipping, sizing, or support: Answer ONLY using the provided context and include citations
                            2. For general greetings or casual conversation: You can respond naturally and friendly
                            3. For questions outside your knowledge base: Politely redirect to relevant policies or suggest contacting support
                            4. Be concise but comprehensive
                            5. Maintain a helpful, professional tone
                            6. The mail should ends with a 
                            Disclaimer:
                                This message was sent from Vellore Institute of Technology.  The contents of this email may contain legally protected confidential or privileged information of “Vellore Institute of Technology”.  
                                If you are not the intended recipient, you should not disseminate, distribute or copy this e-mail. Please notify the sender immediately and destroy all copies of this message and any attachments. 
                                If you have received this email in error, please promptly notify the sender by reply email and delete the original email and any backup copies without reading them.
        """
        

        RAG_Prompt = RAG_Prompt.format(context= context, query = query)
        
        messages=[
            SystemMessage(System_Prompt + "\n\n" + college_context),
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
    
    