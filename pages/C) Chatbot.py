import streamlit as st
import google.generativeai as genai
import os
import requests

try: 
    st.title(":orange[Robot Grrr]")

    someUrl = "https://www.themealdb.com/api/json/v2/1/search.php?s="
    response = requests.get(someUrl)
    data = response.json()
    epiphany = response.text

    promptChar = st.chat_input("Tipy Tapy your Prompt in here >:)")

    realData = data["meals"]
    listOfNames = {}
    
    for name in realData: 
        listOfNames[name["strMeal"]] = name["strInstructions"]
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "answers" not in st.session_state:
        st.session_state.answers = []

    with st.chat_message(name="ai", avatar='🥰'): 
        st.write("Welcome to Hannah and Leah's API AI. Ask away in the box below to get details regarding recipes. If you ask anything else, I, the GREAT Robot Chef, will instead continue redirecting you towards the API.")
    
    key = st.secrets["API_KEY"]
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    if promptChar:
        thing = ""
        definingFactor = ""
        info = ""
        for item, value in listOfNames.items(): 
            if item.lower() in promptChar.lower(): 
                thing = "The Meal"
                definingFactor = item
                info = value
                break
            else: 
                thing = promptChar
                definingFactor = f"If {promptChar} has something relating to food, answer accordingly"
                info = f"Search for whatever the user wants online if it cannot be found using the API."

        responses = model.generate_content(f"You are an expert on food. Respond as if user is a Georgia Tech Computer Science nerd. User has sent the following prompt: {promptChar}. Use the corresponding hidden information given: {thing},{definingFactor},{info}. If {promptChar} is not related to food or recipes at all, respond to them not using the API. However, note that they didn't ask for anything recipe related. Unless the {promptChar} is specifically about food, it's not about a recipe. Remember all the previous questions from {st.session_state.messages}. Also remember {st.session_state.answers}")
        st.session_state.messages += [promptChar]
        st.session_state.answers += [responses.text]


    for i in range(len(st.session_state.messages)):
       with st.chat_message("human", avatar ='🤓'):
           st.write(st.session_state.messages[i])
       with st.chat_message("ai", avatar='🥰'): 
           st.write(st.session_state.answers[i]) 
           
except: 
    st.write(":red[Sorry, Gemini crashed :((( Try refreshing, apologies.]")

