import streamlit as st
import requests as rq

baseUrl = "https://www.themealdb.com/api/json/v1/1/search.php?s="

###2 user interactions (ie. button, slider) --> affect app behavior
##:) One dynamic visual represent (graph, image, plot) --> changes due to user input
##One dynamic chart displaying API data
#Dynamic Chart/protein: 
def protein(): 
    st.header(":red[Meals, Meals, Meals]")
    st.caption(":violet[The API we have used is from The Meals DB, which is a collection of some dishes from around the world, their ingredients, and how to make them. Take a look at how we incorporated it into our work!]")
    tab1, tab2 = st.tabs(["Protein-Specific", "Surf It Yourself!"])
    with tab1: 
        st.header(":blue[Take a closer look at some protein-filled dishes and what areas have more dishes with that protein!]")
        st.markdown('''Choose some options below:''')
        pick_button = st.selectbox("Pick a protein to see more information:", ["Empty", "Chicken", "Beef", "Beans", "Pork", "Fish", "Lamb"], key = "protein")
        favUrl = baseUrl + pick_button
        answer = rq.get(favUrl)
        daReal = answer.json()
        epiphany = answer.text
        if daReal["meals"] == None: 
            st.write("Pick something above to start!")

        if pick_button != 'Empty':
            chickenz = baseUrl + pick_button
            chicky = rq.get(chickenz)
            bReal = chicky.json()
            textReal = bReal["meals"]
            newDict = {}
            for thing in textReal: 
                for item in thing: 
                    if item == "strArea":
                        area = thing[item] 
                        if area in newDict: 
                            newDict[area] += 1
                        else: 
                            newDict[area] = 1
            anotherDict = {"Place": [], "Amount":[]}
            for daKey, daItem in newDict.items(): 
                anotherDict["Place"].append(daKey)
                anotherDict["Amount"].append(daItem)

            st.bar_chart(data = anotherDict, x="Place", y="Amount", color = "#7a2c1b")

    with tab2: 
        st.header(":red[Want to surf the API yourself??? Look no further!]")
        st.markdown(''':rainbow[You can input the part or whole dish name!!! It will show the corresponding dishes, their instructions to make it, and photos. If your input does not match any of our dishes, it will tell you and give you some options.]''')
        search_input = st.text_input("Search for your food:", key = "search")
        if search_input: 
            try: 
                newUrl = baseUrl + search_input
                response = rq.get(newUrl)
                daReal = response.json()
                if search_input != None: 
                    textReal = daReal["meals"]
                    for item in textReal: 
                        st.header(item["strMeal"])
                        st.write(item["strInstructions"])
                        if item["strMealThumb"]: 
                            st.image(item["strMealThumb"], width = 400)
                        else: 
                            st.write(":red[Image Not Found, Google it yourself]")
            except:
                st.header(":violet-background[This food is not in our inventory sorry :(]")
                st.subheader(":violet[You can try some of the following inputs:]")
                st.write(":orange[Escovitch Fish]")
                st.write(":orange[Wontons]")
                st.write(":orange[Shawarma]")
                st.write(":orange[Ribollita]")
                st.write(":orange[Roti John]")
protein()
#Plan: 
#1. Hannah and Leah's favorite meals/dish based on the api --> dynamic chart
#2. Dynamic visuals & data pulled when user searches for meal (if not there, say sorry)
#  - search or select button (food) --> leads to photo and data/instructions
#  - pick a protein (explanation: Leah and Hannah's favorite part of a meal is the protein, we have many options :)
#  -> pick a protein = chicken, beef, beans, pork -> user can choose priten then they can show hannah and leah fav protein from that protein option.
#chicken -> Kung Pao Chicken, beef -> Szechuan beef, beans -> Oxtail with broad beans, pork -> Tonkatsu pork
