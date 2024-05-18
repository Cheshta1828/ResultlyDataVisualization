import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import scipy
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.markdown("<h1 style='text-align: center; color: white;'>Compare two results with Visualizations</h1>", unsafe_allow_html=True)
#state management block starts here
if "selected" not in st.session_state:
    st.session_state.selected = []
if "uploaded" not in st.session_state:  
    st.session_state.uploaded = {}
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
if "list_of_files" not in st.session_state:
    st.session_state.list_of_files = [None,None]
if "columnsoffetched" not in st.session_state:
    st.session_state.columnsoffetched = []
if "columnsofuploaded" not in st.session_state:
    st.session_state.columnsofuploaded = []
if "all_subjects1" not in st.session_state:
    st.session_state.all_subjects1 = []
if "all_subjects2" not in st.session_state:
    st.session_state.all_subjects2 = []
if "buttondisabled" not in st.session_state:
    st.session_state.buttondisabled = False
if "selected_fetched_subjects" not in st.session_state:
    st.session_state.selected_fetched_subjects = []
if "selected_uploaded_subjects" not in st.session_state:
    st.session_state.selected_uploaded_subjects = []
if "already_read" not in st.session_state:
    st.session_state.already_read = []
if "already_fetched" not in st.session_state:
    st.session_state.already_fetched = []
#state management block ends here

#requesting the available results from the resultly server
url = 'https://resultlymsi.pythonanywhere.com/visualize/result/'
response = requests.get(url)
checkboxes_dict = {}
uploaded_and_fetched = {}
col1 , col2 , col3 = st.columns(3)
with col1:
    #Filling up the checkboxes_dict with the fetched results
    options=[f"{item['course_abbreviation']} - {item['semester']} Passout Year: {item['passout_year']} ({item['id']})" for item in response.json()]
    st.header("Fetch an already available result")
    option = st.selectbox("This option fetches already available results from our database:", options)
    col1a , col2a  = st.columns(2)
    with col1a:
        res=st.text_input(value= option,label="You Selected",key=None)
        add_button_clicked=st.button("Add", type="primary")
        for item in st.session_state.selected:
            checkboxes_dict[item] = st.checkbox(item)
        if add_button_clicked:
            selected_id = response.json()[options.index(option)]['id']
            st.session_state.selected.append(res)
            for item in st.session_state.selected:
                try:
                   
                    checkboxes_dict[item] =st.checkbox(item)
                    
                except:
                    continue

    with col2a:
        st.write("")
        
with col2:
    st.write("")
with col3:
    #Uploading the custom result which will be compared with the fetched result
    st.header("Upload any result to compare")
    uploaded_file=st.file_uploader("Upload custom result to visualize and compare it with the fetched data", label_visibility="visible",type=["csv"])
    upload_button_clicked=st.button("Upload", type="primary")
    for item in st.session_state.uploaded:
                checkboxes_dict[item] = st.checkbox(item)
    if upload_button_clicked:
            if uploaded_file is not None:
                st.session_state.uploaded[uploaded_file.name] = uploaded_file
                for item in st.session_state.uploaded:
                    try:
                        checkboxes_dict[item] = st.checkbox(item)
                    except:
                        continue
            else:
                st.write("No file uploaded!Please choose one")
            print("these are the uploaded files",st.session_state.uploaded)
style = "<style>.row-widget.stButton {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)
error=False
st.session_state.buttondisabled=False
with st.empty():
    btn=st.button("Fetch Subjects")
    if btn and not st.session_state.buttondisabled:
        st.session_state.buttondisabled=True
        error=False
        if len([s for s in checkboxes_dict.keys() if checkboxes_dict[s]])>2:
            lstst=[s for s in checkboxes_dict.keys() if checkboxes_dict[s]]
            print(lstst)
            st.error("You can only compare and select 2 results at a time")
            error=True
            # checkboxes_dict[item]=False
        if len([s for s in checkboxes_dict.keys() if checkboxes_dict[s]])<=1:
            lstst=[s for s in checkboxes_dict.keys() if checkboxes_dict[s]]
            print(lstst)
            st.error("Please select 2 results to compare")
            error=True
            # checkboxes_dict[item]=False
               
        if not error:
            for item in checkboxes_dict.keys():
                if not checkboxes_dict[item]:
                    continue
                print("trying to find the item",item)
                if ".csv" in item and item not in st.session_state.already_read:
                    print(st.session_state.uploaded)
                    df=pd.read_csv(st.session_state.uploaded[item])
                    st.session_state.list_of_files[1]=df
                    st.session_state.already_read.append(item)
                elif ".csv" not in item and item not in st.session_state.already_fetched:
                    print("trying to fetch the item",item)
                    print("this was the already fetched",st.session_state.already_fetched)
                    listofstring=item.split(" ")
                    id=listofstring[-1][1:-1]
                    json_response = requests.get(f'https://resultlymsi.pythonanywhere.com/visualize/result/{id}').json()
                    df_file=pd.read_json(json_response['result_json'])
                    st.session_state.list_of_files[0]=df_file
                    st.session_state.already_fetched.append(item)
                    print("appended the fetched file",st.session_state.already_fetched)
              
            st.session_state.columnsoffetched=st.session_state.list_of_files[0].columns[4:]
            st.session_state.columnsoffetched=st.session_state.columnsoffetched[:-4]
            st.session_state.columnsofuploaded =st.session_state.list_of_files[1].columns[4:]
            st.session_state.columnsofuploaded = st.session_state.columnsofuploaded [:-4]
            st.session_state.columnsoffetched=[c for c  in st.session_state.columnsoffetched if 'External' not in c and 'Internal' not in c and 'Total' not in c]
            st.session_state.columnsofuploaded =[c for c in  st.session_state.columnsofuploaded  if 'External' not in c and 'Internal' not in c and 'Total' not in c and '.1' not in c and '.2' not in c]
    elif st.session_state.buttondisabled and btn:
        st.error("Please Refresh")             
                 
col1b , col2b = st.columns(2)
with col1b:
    list_updated=0
    st.markdown("<h4 style=' color: white;'>Fetched Data </h4>", unsafe_allow_html=True)
    option1 = st.selectbox(
    "Select the subject(s) :",st.session_state.columnsoffetched)
    add_button2_clicked=st.button("Add Data 1 Subject", type="primary")
    placeholder=st.empty()
    placeholder.write(st.session_state.s)
    if add_button2_clicked:
        st.session_state.all_subjects1.append(option1)
        if option1 not in st.session_state.selected_subject:
            list_duplicate = st.session_state.selected_subject
            st.session_state.selected_subject.append(option1)
            list_updated=1
            st.session_state.s=""
            for item in st.session_state.selected_subject:
                st.session_state.s=st.session_state.s+"\n"+str(item)
            list_updated=0
            placeholder.text(st.session_state.s)
with col2b:
    st.markdown("<h4 style=' color: white;'>Uploaded Data</h4>", unsafe_allow_html=True)
    option2 = st.selectbox(
    "Selected the subject(s):", st.session_state.columnsofuploaded)
    list_updated=0
    add_button3_clicked=st.button("Add Data 2 subject", type="primary")
    if add_button3_clicked:
        st.session_state.all_subjects2.append(option2) 
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
reappeardict1={}
reappeardict2={}
style = "<style>.row-widget.stButton {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)
if st.button("Compare and visualize!"):
        if len(st.session_state.all_subjects1)==0 or len(st.session_state.all_subjects2)==0:
            st.error("Please add the subjects to compare")
        else:
            Lofdf=[]
            if len(st.session_state.all_subjects1)!= len(st.session_state.all_subjects2):
                st.error("Please select 2 subjects to compare")
            else:
                dfofone={}
                dfoftwo={}
                for subj1 in st.session_state.all_subjects1:
                    index=st.session_state.list_of_files[0].columns.get_loc(subj1)
                    dfofone[subj1]=list(st.session_state.list_of_files[0].iloc[:,index+2][1:])
                for subj2 in st.session_state.all_subjects2:
                    index2=st.session_state.list_of_files[1].columns.get_loc(subj2)
                    dfoftwo[subj2]=list(st.session_state.list_of_files[1].iloc[:,index2+2][1:])
                dfofone=pd.DataFrame(dfofone)
                dfoftwo=pd.DataFrame(dfoftwo)
                no_of_graphs=dfofone.shape[1]
                for i in range(no_of_graphs):
                    subj1 = dfofone.columns[i]
                    subj2 = dfoftwo.columns[i]
                    reappeardict1[subj1]=0
                    reappeardict2[subj2]=0
                    y1 = pd.to_numeric(dfofone.iloc[:, i],errors="coerce").sort_values(ascending=True).reset_index(drop=True)
                    y2 = pd.to_numeric(dfoftwo.iloc[:, i],errors="coerce").sort_values(ascending=True).reset_index(drop=True)
                    x = list(range(1, max(len(y1), len(y2)) + 1))
                    y1 = y1.reindex(range(len(x)))
                    y2 = y2.reindex(range(len(x)))
                    df=pd.DataFrame({"students":x,subj1:y1,subj2:y2})
                    Lofdf.append(df)
                    for index, row in df.iterrows():
                        if row[subj1]<40 and row[subj2]>=40:
                            reappeardict1[subj1]+=1
                        if row[subj1]>=0 and row[subj2]<40:
                            reappeardict2[subj2]+=1
                    df_melted=pd.melt(df,id_vars="students",value_vars=[subj1,subj2],var_name="subjects",value_name="marks")
                    fig=px.line(df_melted,x="students",y="marks",color="subjects",title=f"Comparison of {dfofone.columns[i]} and {dfoftwo.columns[i]}")
                    with st.container():
                        st.plotly_chart(fig,title=f"Comparison of {dfofone.columns[i]} and {dfoftwo.columns[i]}")
                st.markdown("<h5 style=' color: white;'>Number of reapper in all subjects</h2>", unsafe_allow_html=True)      
                col1d , col2d = st.columns(2)
                with col1d:
                    for key in reappeardict1.keys():
                        st.metric(label=f"{key} Reappear", value=reappeardict1[key])
                with col2d:
                    for key in reappeardict2.keys():
                        st.metric(label=f"{key} Reappear", value=reappeardict2[key])
                selected_subjects1 = st.session_state.all_subjects1
                selected_subjects2 = st.session_state.all_subjects2
                selected_subeject = selected_subjects1 + selected_subjects2
                values1 = []
                values2 = []
                if selected_subjects1[0] in st.session_state.list_of_files[0].columns:
                    d1 = st.session_state.list_of_files[0]
                    d2 = st.session_state.list_of_files[1]
                else:
                    d1 = st.session_state.list_of_files[1]
                    d2 = st.session_state.list_of_files[0]
                indexs1 = [d1.columns.get_loc(subj) for subj in selected_subjects1]
                indexs2 = [d2.columns.get_loc(subj) for subj in selected_subjects2]
                for index in indexs1:
                    values1.append(d1.iloc[1:,index].astype(float).mean())
                    values1.append(d2.iloc[1:,index].astype(float).mean())
                for index in indexs2:
                    values2.append(d1.iloc[1:,index+1].astype(float).mean())
                    values2.append(d2.iloc[1:,index+1].astype(float).mean())
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=selected_subeject,
                    y=values1,
                    name='Internal'))
                fig.add_trace(go.Bar(
                    x=selected_subeject,
                    y=values2,
                    name='External'
                )) 
                fig.update_layout(barmode='stack', title='Internal - External marks comparison of all the subjects')
                st.plotly_chart(fig)       
                
                for i in range(no_of_graphs):
                    subj1=Lofdf[i].columns[1]
                    subj2=Lofdf[i].columns[2]
                    graddict1={
                                'O':{},
                                'A':{},
                                'B':{},
                                'C':{},
                                'D':{},
                                'F':{}}
                    graddict2={
                                'O':{},
                                'A':{},
                                'B':{},
                                'C':{},
                                'D':{},
                                'F':{}}
                    graddict1['O'][subj1]=0
                    graddict1['A'][subj1]=0
                    graddict1['B'][subj1]=0
                    graddict1['C'][subj1]=0
                    graddict1['D'][subj1]=0
                    graddict1['F'][subj1]=0
                    graddict2['O'][subj2]=0
                    graddict2['A'][subj2]=0
                    graddict2['B'][subj2]=0
                    graddict2['C'][subj2]=0
                    graddict2['D'][subj2]=0
                    graddict2['F'][subj2]=0
                    for index, row in Lofdf[i].iterrows():
                        if row[subj1]>=90:
                            graddict1['O'][subj1]+=1
                        elif row[subj1]>=75 and row[subj1]<90:
                            graddict1['A'][subj1]+=1
                        elif row[subj1]>=60 and row[subj1]<75:
                            graddict1['B'][subj1]+=1
                        elif row[subj1]>=50 and row[subj1]<60:
                            graddict1['C'][subj1]+=1
                        elif row[subj1]>=40 and row[subj1]<50:
                            graddict1['D'][subj1]+=1
                        else:
                            graddict1['F'][subj1]+=1
                        if row[subj2]>=90:
                            graddict2['O'][subj2]+=1
                        elif row[subj2]>=75 and row[subj2]<90:
                            graddict2['A'][subj2]+=1
                        elif row[subj2]>=60 and row[subj2]<75:
                            graddict2['B'][subj2]+=1
                        elif row[subj2]>=50 and row[subj2]<60:
                            graddict2['C'][subj2]+=1
                        elif row[subj2]>=40 and row[subj2]<50:
                            graddict2['D'][subj2]+=1
                        else:
                            graddict2['F'][subj2]+=1
                    grades_df = pd.DataFrame({
                'Grade': ['O', 'A', 'B', 'C', 'D', 'F'],
                subj1: [graddict1[grade][subj1] for grade in ['O', 'A', 'B', 'C', 'D', 'F']],
                subj2: [graddict2[grade][subj2] for grade in ['O', 'A', 'B', 'C', 'D', 'F']]})
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=grades_df['Grade'],
                        y=grades_df[subj1],
                        name=subj1))
                    fig.add_trace(go.Bar(
                        x=grades_df['Grade'],
                        y=grades_df[subj2],
                        name=subj2))
                    fig.update_layout(
                        title='Grade Distribution Comparison',
                        xaxis=dict(title='Grade'),
                        yaxis=dict(title='Number of Students'),
                        barmode='group')
                    with st.container(): 
                        st.plotly_chart(fig)
            

        