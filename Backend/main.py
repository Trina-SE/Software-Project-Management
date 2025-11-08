import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(msg: Message):
    try:
        # Enhanced prompt for better formatted responses
        enhanced_prompt = f"""Please provide a clear, well-organized response to: "{msg.message}"

CRITICAL FORMATTING RULES - FOLLOW THESE EXACTLY:
• Use **bold** for important terms and headings
• Use ### for main section headings
• Use ## for subsection headings
• Use numbered lists (1. 2. 3.) for steps
• Use proper paragraph breaks with blank lines
• For code blocks, use ```python and ``` with proper indentation
• Keep technical explanations simple but accurate and short
• Structure responses with clear sections

STRICTLY AVOID:
• Using *• combinations (this creates ugly formatting)
• Random asterisks anywhere in text
• Using * for bullet points
• Poorly formatted lists
• Walls of text without breaks
• Any markdown syntax that creates visual clutter
• Inconsistent indentation in code blocks

For code explanations:
• Use clear numbered sections (1. 2. 3.)
• Explain each part step by step
• Use proper code block formatting with ```python
• Keep code indentation clean and readable
• Use bullet points for detailed explanations within sections

Response Structure:
1. Use numbered sections for main parts
2. Explain code components easily
3. Include practical examples where relevant

Question: {msg.message}"""

        response = model.generate_content(enhanced_prompt)

        # Clean and format the response
        formatted_response = response.text.strip()

        # Basic formatting improvements
        formatted_response = formatted_response.replace('\n\n\n', '\n\n')  # Remove excessive line breaks
        formatted_response = formatted_response.replace('* ', '• ')  # Convert asterisks to bullets
        formatted_response = formatted_response.replace('- ', '• ')  # Convert dashes to bullets
        formatted_response = formatted_response.replace('*•', '')  # Remove *• combinations
        formatted_response = formatted_response.replace('**', '**')  # Ensure proper bold markers

        # Ensure proper spacing
        lines = formatted_response.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)

        formatted_response = '\n\n'.join(cleaned_lines)

        return {"response": formatted_response}
    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)