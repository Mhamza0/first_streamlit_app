import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import  URLError
streamlit.title('My Parent New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale , Spinach & Rocket smoothie')
streamlit.text('🐔 Hard Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')   
#import pandas
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#put a fruits list
#streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index))
#Display the table on the page
fruit_selected=streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruit_selected]
streamlit.dataframe(fruits_to_show)

#create the repeatable code block(function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
    fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#New section to display
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about ?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()



#import snowflake.connector
streamlit.header("View our Fruit List - Add your favourites!:")
#snowflake related function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return  my_cur.fetchall()
# add a button
if streamlit.button('Get fruit list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)



def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('kiwi')")
         return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

streamlit.stop()
#streamlit.write('Thanks for adding',add_my_fruit)
