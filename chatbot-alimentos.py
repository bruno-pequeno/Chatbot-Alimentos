import google.generativeai as genai
import gradio as gr
import os

class FoodChatbot:
    def __init__(self):
        genai.configure(api_key="API_KEY")
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_response(self, user_input):
        try:
            template = f"""
            Sobre {user_input}:

            **Nutrientes:**
            {{nutrientes}}

            **Benefícios:**
            {{beneficios}}

            **Receita simples**
            **Ingredientes:**
            {{ingredientes}}

            **Preparo:**
            {{preparo}}
            """
            
            response = self.model.generate_content(
                template,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1000
                )
            )
            
            return response.text.strip()
        except Exception as e:
            return f"Erro: {str(e)}"

def create_interface():
    chatbot = FoodChatbot()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    bot_icon = os.path.join(current_dir, "assets", "robo-do-usuario.png")
    user_icon = os.path.join(current_dir, "assets", "usuario-do-circulo.png")
    
    with gr.Blocks(theme=gr.themes.Soft(
        text_size="lg",
        spacing_size="sm",
    )) as interface:
        gr.Markdown("### 🍎 **Chatbot de Alimentos**")
        
        chatbot_ui = gr.Chatbot(
            height=400,
            bubble_full_width=False,
            show_label=True,
            avatar_images=[user_icon, bot_icon], 
            render_markdown=True,
        )
        
        msg_input = gr.Textbox(
            placeholder="Digite o nome de um alimento...",
            label="Mensagem",
            scale=4
        )
        
        def respond(message, history):
            if not message.strip(): 
                return "", history
            
            bot_response = chatbot.generate_response(message)
            history.append((message, bot_response))
            return "", history
        
        msg_input.submit(respond, [msg_input, chatbot_ui], [msg_input, chatbot_ui])
        gr.Button("Enviar", scale=1).click(respond, [msg_input, chatbot_ui], [msg_input, chatbot_ui])
    
    return interface

if __name__ == "__main__":
    create_interface().launch()
