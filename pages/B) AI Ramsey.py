import streamlit as st
import google.generativeai as genai
import os
import requests as rq

key = st.secrets["MY_KEY"]
genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-1.5-flash") #this is the free model of google gemini

baseUrl = "https://www.themealdb.com/api/json/v2/1/search.php?s="
answer = rq.get(baseUrl)
daReal = answer.json()
epiphany = answer.text

james = st.selectbox("What level of difficulty are you feeling today?", ["Choose one", "Easy", "Medium", "Hard"])
kiernan = st.selectbox("How do you want your meal cooked? >:)", ["Choose a Difficulty", "Fry", "Grill", "Stir"])
buttonWow = st.button("Press me when done!")

if buttonWow and james != "Choose one" and kiernan != "Choose a Difficulty": 
    data = daReal["meals"]
    newList = []
    for index,length in enumerate(data):
        if kiernan.lower() in length["strInstructions"].lower(): 
            newList.append((len(length["strInstructions"]),index))

    midPoint = int(len(newList)/2)

    length = 10000
    length2 = 0
    if james == "Easy": 
        for item in newList: 
            first = item[0]
            second = item[1]
            if first < length: 
                thing = second
            else: 
                continue
    elif james == "Medium": 
        thing = newList[midPoint][1]
    elif james == "Hard": 
        for item in newList: 
            first = item[0]
            second = item[1]
            if first > length2: 
                thing = second

    st.header(data[thing]["strMeal"])
    st.write(":green[by Gemini Gordan Ramsey]")
    script = data[thing]["strInstructions"]
    response = model.generate_content(f"Pretend to be Gordan Ramsey WITHOUT SWEAR WORDS OR CURSING instructing the user on a {james} type meal using the {script} as the base instruction.") 
    st.write(response.text)

else: 
    st.write(":violet[You have to choose something in the selectbox first!]")


#selectbox (easy, mid, hard: len(strInstructions)); some ingredients they like (text input) 
#



