import streamlit as st
import requests
import json
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.markdown("<h1 style='text-align: center; color: white;'>Data Visualization</h1>", unsafe_allow_html=True)
col1 , col2 , col3 = st.columns(3)
if "selected" not in st.session_state:
    st.session_state.selected = []
if "uploaded" not in st.session_state:  
    st.session_state.uploaded = []
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = []
if "s" not in st.session_state:
    st.session_state.s = ""
if "str2" not in st.session_state:
    st.session_state.str2 = ""
if "selected_subject2" not in st.session_state:
    st.session_state.selected_subject2 = []
if "checked_items" not in st.session_state:
    st.session_state.checked_items = []
print("hello")
url = 'https://resultlymsi.pythonanywhere.com/visualize/result/'
response = requests.get(url)
with col1:
    options=[f"Course : {(requests.get('https://resultlymsi.pythonanywhere.com/visualize/getcourse/7').json())['abbreviation']} , Semester: {item['semester']}, Passout Year: {item['passout_year']}" for item in response.json()]
    st.header("Fetch data")
    option = st.selectbox("Selected an already available result:", options)
    col1a , col2a  = st.columns(2)
    with col1a:
        res=st.text_input(value= option,label="You Selected",key=None)
        add_button_clicked=st.button("Add", type="primary")
        for item in st.session_state.selected:
                st.checkbox(item)
        if add_button_clicked:
            st.session_state.selected.append(res)
            for item in st.session_state.selected:
                try:
                    st.checkbox(item)
                except:
                    continue
        
    with col2a:
        st.write("")
        
with col2:
    st.write("")
with col3:
    st.header("Upload data")
    uploaded_file=st.file_uploader("Upload custom result to visualize", label_visibility="visible",type=["csv"])
    upload_button_clicked=st.button("Upload", type="primary")
    for item in st.session_state.uploaded:
                st.checkbox(item)
                
    if upload_button_clicked:
            if uploaded_file is not None:
                st.session_state.uploaded.append(uploaded_file.name)
                for item in st.session_state.uploaded:
                    try:
                        st.checkbox(item)
                    except:
                        continue
                    
            else:
                st.write("No file uploaded!Please choose one")
                
col1b , col2b = st.columns(2)
with col1b:
    list_updated=0
    st.markdown("<h4 style=' color: white;'>Data 1</h4>", unsafe_allow_html=True)
    option1 = st.selectbox(
    "Select the subject(s) :",
    ("Data Visualization", "TC", "Web Tech"))
    add_button2_clicked=st.button("Add Data 1 Subject", type="primary")
    placeholder=st.empty()
    placeholder.write(st.session_state.s)
    if add_button2_clicked:
        if option1 not in st.session_state.selected_subject:
            list_duplicate = st.session_state.selected_subject
            st.session_state.selected_subject.append(option1)
            list_updated=1
            print("list_updated",list_updated)
            print("list_duplicate",list_duplicate)
            print(st.session_state.selected_subject)
            st.session_state.s=""
            for item in st.session_state.selected_subject:
                
            
                st.session_state.s=st.session_state.s+"\n"+str(item)
                
            
            list_updated=0
            
            placeholder.text(st.session_state.s)
            print("list_updatedafter",list_updated)
            
with col2b:
    st.markdown("<h4 style=' color: white;'>Data 2</h4>", unsafe_allow_html=True)
    option2 = st.selectbox(
    "Selected the subject(s):",
    ("Fit", "SE", "AI"))
    list_updated=0
    add_button3_clicked=st.button("Add Data 2 subject", type="primary")
    placeholder2=st.empty()
    placeholder2.write(st.session_state.str2)
    if add_button3_clicked:
        if option2 not in st.session_state.selected_subject2:
            list_duplicate = st.session_state.selected_subject2
            st.session_state.selected_subject2.append(option2)
            list_updated=1
            st.session_state.str2=""
            for item in st.session_state.selected_subject2:
                
            
                st.session_state.str2=st.session_state.str2+"\n"+str(item)
                
            
            list_updated=0
            
            placeholder2.text(st.session_state.str2)
            print("list_updatedafter",list_updated)
            
            

style = "<style>.row-widget.stButton {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)
with st.empty():
    if st.button("Compare Now!"):
        pass