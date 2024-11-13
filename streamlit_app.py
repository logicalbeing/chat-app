import streamlit as st
import os
import google.generativeai as genai



# Function to display the login page
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    mobile = st.text_input("Mobile")
    password = st.text_input("Password", type="password")
    language = st.selectbox("Preferred Language", ["English", "Telugu"])


    # Check if password is valid (not blank)
    if st.button("Login"):
        if username and mobile:
            if password:
                st.session_state['gemini_api_key'] = password
            st.session_state['username'] = username
            st.session_state['mobile'] = mobile
            st.session_state['password'] = password
            st.session_state['language'] = language
            st.session_state['step'] = 0
            st.session_state['responses'] = {}
            st.success("Login successful!")
        else:
            st.error("Please fill all fields.")



# Translations for headers and questions (example translations)
def translate_header(header, language):
    translations = {
        "Greeting": "స్వాగతం",
        "Daily Check-In": "రోజు విచారణ",
        "Blood Sugar Level": "రక్త చక్కెర స్థాయి",
        "Physical Feelings": "శారీరక అనుభవాలు",
        "Emotional State": "మానసిక స్థితి",
        "Stress Level": "ఒత్తిడి స్థాయి",
        "Sources of Stress": "ఒత్తిడి మూలాలు",
        "Sharing Thoughts": "ఆలోచనలను పంచుకోండి",
        "Coping with Stress": "ఒత్తిడి ఎదుర్కోవడం",
        "Stress Relief Tips": "ఒత్తిడి ఉపశమనం చిట్కాలు",
        "Acknowledgment": "ప్రశంస",
        "Stress Relief Activities": "ఒత్తిడి ఉపశమనం కార్యకలాపాలు",
        "Meals": "భోజనాలు",
        "Exercise": "వ్యాయామం",
        "Setting a Goal": "లక్ష్యం నిర్ణయించడం",
        "Closing Message": "ముగింపు సందేశం"
    }
    return translations.get(header, header) if language == "Telugu" else header

def translate_question(question, language):
    translations = {
        "Hi! How are you today?": "నమస్తే! మీరు ఎలా ఉన్నారు?",
        "How's your day going so far?": "ఇప్పటి వరకు మీ రోజు ఎలా సాగుతోంది?",
        "What's your blood sugar level today - fasting and 2 hours after a meal?": "ఈ రోజు మీ రక్తంలో చక్కెర స్థాయి ఎంత - ఫాస్టింగ్ & భోజనం తర్వాత 2 గంటలు?",
        "How have you been feeling physically? Any symptoms you'd like to mention?": "మీరు శారీరకంగా ఎలా ఉన్నారు? మీరు చెప్పాలనుకుంటున్న ఎలాంటి లక్షణాలు ఉన్నాయా?",
        "Have you been feeling down, anxious, or stressed lately? Would you like to talk about it?": "మీరు ఇటీవల దిగజారిన, ఆందోళనలో ఉన్న లేదా ఒత్తిడిలో ఉన్నారా? మీరు దాని గురించి మాట్లాడాలనుకుంటున్నారా?",
        "On a scale of 1-10, how stressed are you today?": "మీరు ఈ రోజు ఎంత ఒత్తిడిలో ఉన్నారు? 1-10 లో మాపండి.",
        "What's been causing you stress lately? (Work, family, health, money, etc.)": "మీకు_recent ఒత్తిడి కలిగించే అంశాలు ఏమిటి? (పని, కుటుంబం, ఆరోగ్యం, డబ్బు, మొదలైనవి?)",
        "Is there anything on your mind you'd like to share? I'm here to listen.": "మీకు చెప్పాలనుకుంటున్న ఏదైనా మీ మనసులో ఉందా? నేను వినడానికి ఇక్కడ ఉన్నాను.",
        "How have you been dealing with stress? Is it working?": "మీరు ఒత్తిడిని ఎలా ఎదుర్కొంటున్నారు? ఇది పనిచేస్తున్నదా?",
        "Do you want some tips to manage stress? Here are a few- [deep breathing, a walk, talking to someone.]": "మీరు ఒత్తిడిని నిర్వహించడానికి కొన్ని చిట్కాలు కావాలా? ఇక్కడ కొన్ని ఉన్నాయి - [గాఢ శ్వాస, నడక, ఎవరో మాట్లాడడం.]",
        "It's okay to feel stressed sometimes. You're doing your best, and that matters.": "కొన్నిసార్లు ఒత్తిడిగా భావించడం సరే. మీరు మీ ఉత్తమమైనది చేస్తున్నారు, మరియు అది ముఖ్యం.",
        "Did you try any stress relief activities today? Did they help?": "మీరు ఈ రోజు ఒత్తిడి ఉపశమనం కార్యకలాపాలను ప్రయత్నించారా? అవి సహాయపడాయా?",
        "How have your meals been today? Eating healthy?": "ఈ రోజు మీ భోజనాలు ఎలా ఉన్నాయి? ఆరోగ్యకరమైన ఆహారం తింటున్నారా?",
        "Did you get some exercise today? How was it?": "మీరు ఈ రోజు కొంత వ్యాయామం చేసారా? అది ఎలా ఉంది?",
        "Let's set a small goal for tomorrow to manage stress. What could make a positive difference?": "ఒత్తిడిని నిర్వహించడానికి రేపు చిన్న లక్ష్యం పెట్టుకుందాం. ఇది సానుకూల మార్పు కలిగించగలదా?",
        "Thanks for chatting with me today. Remember, you're not alone. Take care, and we'll talk again soon!": "ఈ రోజు నాతో మాట్లాడటానికి ధన్యవాదాలు. మీరు ఒంటరిగా లేరు. జాగ్రత్తగా ఉండండి, మళ్లీ త్వరలో మాట్లాడుదాం!"
    }
    return translations.get(question, question) if language == "Telugu" else question

# Detailed questions with icons and types
questions = [
    ("Greeting", "😀", "text", "Hi! How are you today?", "q1"),
    ("Daily Check-In", "☀️", "text_area", "How's your day going so far?", "q2"),
    ("Blood Sugar Level", "🩸", "text_area", "What's your blood sugar level today - fasting and 2 hours after a meal?", "q3"),
    ("Physical Feelings", "🤒", "text_area", "How have you been feeling physically? Any symptoms you'd like to mention?", "q4"),
    ("Emotional State", "😔", "text_area", "Have you been feeling down, anxious, or stressed lately? Would you like to talk about it?", "q5"),
    ("Stress Level", "📊", "slider", "On a scale of 1-10, how stressed are you today?", "q6"),
    ("Sources of Stress", "💼", "text_area", "What's been causing you stress lately? (Work, family, health, money, etc.)", "q7"),
    ("Sharing Thoughts", "💬", "text_area", "Is there anything on your mind you'd like to share? I'm here to listen.", "q8"),
    ("Coping with Stress", "🧘‍♂️", "text_area", "How have you been dealing with stress? Is it working?", "q9"),
    ("Stress Relief Tips", "💡", "text_area", "Do you want some tips to manage stress? Here are a few- [deep breathing, a walk, talking to someone.]", "q10"),
    ("Acknowledgment", "❤️", "text_area", "It's okay to feel stressed sometimes. You're doing your best, and that matters.", "q11"),
    ("Stress Relief Activities", "✅", "text_area", "Did you try any stress relief activities today? Did they help?", "q12"),
    ("Meals", "🥗", "text_area", "How have your meals been today? Eating healthy?", "q13"),
    ("Exercise", "🏋️‍♀️", "text_area", "Did you get some exercise today? How was it?", "q14"),
    ("Setting a Goal", "🎯", "text_area", "Let's set a small goal for tomorrow to manage stress. What could make a positive difference?", "q15"),
    ("Closing Message", "👋", "text", "Thanks for chatting with me today. Remember, you're not alone. Take care, and we'll talk again soon!", "q16")
]

# Function to generate the summary using the Gemini API
def generate_summary(chat_history):
    genai.configure(api_key=st.session_state.gemini_api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')  # Use the appropriate model
    response = model.generate_content(f"""
    You are a diabetes expert who is reviewing a patient's survey responses. The patient has shared detailed information 
    about their daily health, including their blood sugar levels and stress levels. Based on this survey data, 
    please summarize the patient's responses in a detailed manner, paying particular attention to the following key areas:

    1. **Blood Sugar Levels**: Summarize any information the patient provided regarding their blood sugar levels, 
       including fasting and post-meal readings, any fluctuations or concerns they mentioned.
    2. **Stress Levels**: Summarize the patient's stress levels, including any stress-related symptoms, causes of stress 
       (e.g., work, family, health, etc.), and how they are coping with it.
    
    After summarizing, provide actionable **next steps** for the patient:
    
    - Specific recommendations for managing blood sugar (e.g., dietary changes, exercise, medication adjustments).
    - Tips for reducing stress and improving mental well-being (e.g., relaxation techniques, stress management activities, 
      seeking support).
    - Any potential follow-up actions that might be needed (e.g., follow-up surveys, monitoring stress triggers, etc.).
    
    Use a tone that is empathetic, professional, and supportive. The goal is to provide the patient with practical advice 
    to help them manage both their blood sugar and stress more effectively.
    Translations are provided for your reference 
        "Hi! How are you today?": "నమస్తే! మీరు ఎలా ఉన్నారు?",
        "How's your day going so far?": "ఇప్పటి వరకు మీ రోజు ఎలా సాగుతోంది?",
        "What's your blood sugar level today - fasting and 2 hours after a meal?": "ఈ రోజు మీ రక్తంలో చక్కెర స్థాయి ఎంత - ఫాస్టింగ్ & భోజనం తర్వాత 2 గంటలు?",
        "How have you been feeling physically? Any symptoms you'd like to mention?": "మీరు శారీరకంగా ఎలా ఉన్నారు? మీరు చెప్పాలనుకుంటున్న ఎలాంటి లక్షణాలు ఉన్నాయా?",
        "Have you been feeling down, anxious, or stressed lately? Would you like to talk about it?": "మీరు ఇటీవల దిగజారిన, ఆందోళనలో ఉన్న లేదా ఒత్తిడిలో ఉన్నారా? మీరు దాని గురించి మాట్లాడాలనుకుంటున్నారా?",
        "On a scale of 1-10, how stressed are you today?": "మీరు ఈ రోజు ఎంత ఒత్తిడిలో ఉన్నారు? 1-10 లో మాపండి.",
        "What's been causing you stress lately? (Work, family, health, money, etc.)": "మీకు_recent ఒత్తిడి కలిగించే అంశాలు ఏమిటి? (పని, కుటుంబం, ఆరోగ్యం, డబ్బు, మొదలైనవి?)",
        "Is there anything on your mind you'd like to share? I'm here to listen.": "మీకు చెప్పాలనుకుంటున్న ఏదైనా మీ మనసులో ఉందా? నేను వినడానికి ఇక్కడ ఉన్నాను.",
        "How have you been dealing with stress? Is it working?": "మీరు ఒత్తిడిని ఎలా ఎదుర్కొంటున్నారు? ఇది పనిచేస్తున్నదా?",
        "Do you want some tips to manage stress? Here are a few- [deep breathing, a walk, talking to someone.]": "మీరు ఒత్తిడిని నిర్వహించడానికి కొన్ని చిట్కాలు కావాలా? ఇక్కడ కొన్ని ఉన్నాయి - [గాఢ శ్వాస, నడక, ఎవరో మాట్లాడడం.]",
        "It's okay to feel stressed sometimes. You're doing your best, and that matters.": "కొన్నిసార్లు ఒత్తిడిగా భావించడం సరే. మీరు మీ ఉత్తమమైనది చేస్తున్నారు, మరియు అది ముఖ్యం.",
        "Did you try any stress relief activities today? Did they help?": "మీరు ఈ రోజు ఒత్తిడి ఉపశమనం కార్యకలాపాలను ప్రయత్నించారా? అవి సహాయపడాయా?",
        "How have your meals been today? Eating healthy?": "ఈ రోజు మీ భోజనాలు ఎలా ఉన్నాయి? ఆరోగ్యకరమైన ఆహారం తింటున్నారా?",
        "Did you get some exercise today? How was it?": "మీరు ఈ రోజు కొంత వ్యాయామం చేసారా? అది ఎలా ఉంది?",
        "Let's set a small goal for tomorrow to manage stress. What could make a positive difference?": "ఒత్తిడిని నిర్వహించడానికి రేపు చిన్న లక్ష్యం పెట్టుకుందాం. ఇది సానుకూల మార్పు కలిగించగలదా?",
        "Thanks for chatting with me today. Remember, you're not alone. Take care, and we'll talk again soon!": "ఈ రోజు నాతో మాట్లాడటానికి ధన్యవాదాలు. మీరు ఒంటరిగా లేరు. జాగ్రత్తగా ఉండండి, మళ్లీ త్వరలో మాట్లాడుదాం!"
                                  
    Reply in the language of the patient.
    Here's the patient's survey data:
    {chat_history}
    """)
    return response.text

# Function to display the survey questions
def survey():
    # Get the current step and language
    step = st.session_state.get('step', 0)
    language = st.session_state.get('language', 'English')

    # Calculate and display progress bar
    progress = int((step + 1) / len(questions) * 100)  # Convert to integer
    st.progress(progress)

    # Get the question, icon, input type, and id for the current step
    question_header, icon, input_type, detailed_question, question_id = questions[step]

    # Translate header and question
    header = translate_header(question_header, language)
    question = translate_question(detailed_question, language)

    # Display the header with the icon
    st.header(f"{icon} {header}")

    # Display the input field for the question based on its type
    response = None
    if input_type == "text":
        response = st.text_input(question, value=st.session_state['responses'].get(question_id, ''))
    elif input_type == "text_area":
        response = st.text_area(question, value=st.session_state['responses'].get(question_id, ''))
    elif input_type == "slider":
        response = st.slider(question, 1, 10, value=st.session_state['responses'].get(question_id, 1))

    # Save the response when the user clicks the "Next" button
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Previous"):
            if step > 0:
                st.session_state['step'] -= 1
    with col2:
        next_button = st.button("Next")
        if next_button:
            if response:  # Ensure there is a response before moving forward
                st.session_state['responses'][question_id] = response
                if step < len(questions) - 1:
                    st.session_state['step'] += 1
                else:
                    st.success("Survey Completed! Thank you.")
                    show_summary()

# Function to show the entire transcript of responses and the generated summary
def show_summary():
    responses = st.session_state['responses']
    language = st.session_state.get('language', 'English')

    # Step 1: Show the entire transcript of responses
    st.header("Survey Transcript")
    for question_header, _, _, detailed_question, question_id in questions:
        question = translate_question(detailed_question, language)
        response = responses.get(question_id, 'No response')
        st.write(f"**{question}**")
        st.write(f"Response: {response}")
        st.write("---")

    # Check if the password is provided
    if st.session_state.get('password'):
        # Step 2: Generate the summary based on responses only if password is provided
        # Construct the chat history for the Gemini model
        chat_history = ""
        for question_header, _, _, detailed_question, question_id in questions:
            question = translate_question(detailed_question, language)
            response = responses.get(question_id, 'No response')
            chat_history += f"{question}\nResponse: {response}\n\n"

        # Generate the summary using the Gemini model
        with st.spinner("Generating summary..."):
            summary = generate_summary(chat_history)
        
        # Display the generated summary
        st.header("Summary of Your Survey")
        st.write(summary)
    else:
        st.warning("Password not provided. AI summary will not be displayed.")

    # Button to resubmit survey
    if st.button("Resubmit Survey"):
        st.session_state['step'] = 0
        st.session_state['responses'] = {}
        st.experimental_rerun()

# Main function to run the app
def main():
    if 'username' not in st.session_state:
        login()
    else:
        survey()

if __name__ == "__main__":
    main()
