class SimpleChatbot:
    def __init__(self):
        self.responses = {
            "oi": "Oi! Tudo bem?",
            "tudo bem": "Estou bem, obrigado por perguntar! E você?",
            "como vai": "Estou indo bem! E você?",
            "e você": "Eu também estou ótimo, obrigado!",
        }

    def get_response(self, message):
        message = message.lower()
        for key in self.responses:
            if key in message:
                return self.responses[key]
        return "Desculpe, não entendi."

# Exemplo de uso do chatbot
bot = SimpleChatbot()

# Simulação de conversa
while True:
    user_input = input("Você: ")
    if user_input.lower() in ["sair", "exit"]:
        print("Bot: Tchau! Até mais!")
        break
    response = bot.get_response(user_input)
    print("Bot:", response)
