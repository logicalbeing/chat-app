import streamlit
from google.generativeai import Model

# Initialize the generative model (make sure you use the correct model ID)
model = Model('models/gemini-1.5-flash-latest')

# Define the prompt for generating content
prompt = """
You are a diabetes expert reviewing a patient's survey responses about their health, including their blood sugar levels 
and stress levels. Please summarize the responses and provide next steps for managing blood sugar and stress.
"""

# Generate content using the model
response = model.generate_content(prompt)

# Print the generated response
st.print(response.text)
