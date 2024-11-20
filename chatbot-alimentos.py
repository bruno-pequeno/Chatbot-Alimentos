import google.generativeai as genai
import gradio as gr
import os

CONFIG = {
    "model_name": "gemini-1.0-pro",
    "temperature": 0.7,
    "max_output_tokens": 1000
}

class FoodChatbot:
    def __init__(self, config):
        genai.configure(api_key='CHAVE_API')

        self.generation_config = {
            "temperature": config["temperature"],
            "max_output_tokens": config["max_output_tokens"]
        }

        self.safety_settings = {
            "harassment": "block_none",
            "hate": "block_none",
            "sexual": "block_none",
            "dangerous": "block_none"
        }

        self.model = genai.GenerativeModel(
            model_name=config["model_name"],
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        self.chat = self.model.start_chat(history=[])

    def generate_response(self, food_name):
        """Generate detailed food information using Gemini"""
        try:
            prompt = f"""
            Forneça informações detalhadas sobre {food_name} no seguinte formato, em português:

            **Benefícios Nutricionais**:
            - Vitaminas e minerais presentes
            - Calorias e macronutrientes

            **Benefícios para a Saúde**:
            - Liste 3-4 benefícios principais
            - Quem mais se beneficia

            **Receita Simples**:
            Ingredientes:
            - Liste os ingredientes com quantidades

            Modo de Preparo:
            - Descreva os passos numerados
            """

            response = self.chat.send_message(prompt)
            return response.text
        
        except Exception as e:
            return f"Erro ao gerar resposta: {str(e)}"

def create_gradio_interface(chatbot):
    """Create Gradio interface for the food chatbot"""
    return gr.Interface(
        fn=chatbot.generate_response,
        inputs=gr.Textbox(
            lines=1,
            placeholder="Digite um alimento (ex: uva, maçã, banana)",
            label="Nome do Alimento"
        ),
        outputs=gr.Textbox(
            lines=12,
            label="Informações sobre o Alimento"
        ),
        title="🍎 Chatbot de Alimentos - Nutrição e Receitas",
        description="Digite o nome de um alimento para descobrir seus benefícios nutricionais, benefícios para a saúde e uma receita simples.",
        cache_examples=True,
        theme="default"
    )

def main():
    food_chatbot = FoodChatbot(CONFIG)
    
    demo = create_gradio_interface(food_chatbot)
    demo.launch()

if __name__ == "__main__":
    main()