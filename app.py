import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
# import plotly.figure_factory as fF
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.markdown("<h1 style='text-align: center; color: white;'>Data Visualization</h1>", unsafe_allow_html=True)
col1 , col2 , col3 = st.columns(3)
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
    st.session_state.list_of_files = []
if "columnsoffetched" not in st.session_state:
    st.session_state.columnsoffetched = []
if "columnsofuploaded" not in st.session_state:
    st.session_state.columnsofuploaded = []
if "all_subjects1" not in st.session_state:
    st.session_state.all_subjects1 = []
if "all_subjects2" not in st.session_state:
    st.session_state.all_subjects2 = []
    
url = 'https://resultlymsi.pythonanywhere.com/visualize/result/'
response = requests.get(url)
checkboxes_dict = {}

with col1:
    options=[f"{item['course_abbreviation']} - {item['semester']} Passout Year: {item['passout_year']} ({item['id']}) " for item in response.json()]
    #options=["hello","world","this","is","a","test","to","check","the","functionality","of","the","app"]
    st.header("Fetch data")
    option = st.selectbox("Selected an already available result:", options)
    # selected_id = response.json()[options.index(option)]['id']
    col1a , col2a  = st.columns(2)
    with col1a:
        res=st.text_input(value= option,label="You Selected",key=None)
        
        add_button_clicked=st.button("Add", type="primary")
        for item in st.session_state.selected:
                
                checkboxes_dict[item] = st.checkbox(item)
        if add_button_clicked:
            #append the selected file 's id in the list of files column by converting it to csv
            selected_id = response.json()[options.index(option)]['id']
            st.session_state.selected.append(res)
           
            
            
            for item in st.session_state.selected:
                try:
                    checkboxes_dict[item] =st.checkbox(item)
                    
                except:
                    continue
        #print(checkboxes_dict)
        
    with col2a:
        st.write("")
        
with col2:
    st.write("")
with col3:
    st.header("Upload data")
    uploaded_file=st.file_uploader("Upload custom result to visualize", label_visibility="visible",type=["csv"])
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
                
style = "<style>.row-widget.stButton {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)
error=False
with st.empty():
    if st.button("Fetch Subjects"):
        
        error=False
        
        #print("--------checkboxdict",checkboxes_dict)
        for item in  checkboxes_dict:
                # st.session_state.checked_items.append(item)
                if len([s for s in checkboxes_dict.keys() if checkboxes_dict[s]])>2:
                    lstst=[s for s in checkboxes_dict.keys() if checkboxes_dict[s]]
                    print("lstst",lstst)
                    #print([s for s in checkboxes_dict.keys()])
                    #pop up the error message and do not move forward with the code
                    st.error("You can only select 2 subjects at a time")
                    error=True
                    # st.session_state.checked_items.pop(0)
                    checkboxes_dict[item]=False
        if not error:
            
            for item in checkboxes_dict.keys():
                if ".csv" in item:
                    print("in")
                    df=pd.read_csv(st.session_state.uploaded[item])
                    print("inss")
                    st.session_state.list_of_files.append(df)
                    
                else:
                    listofstring=item.split(" ")
                    id=listofstring[-1][1:-1]
                    response = requests.get(f'https://resultlymsi.pythonanywhere.com/visualize/result/{id}')
                    for item in response.json():
                        df_file=pd.read_json(item['result_json'])
                        st.session_state.list_of_files.append(df_file)
              
            st.session_state.columnsoffetched=st.session_state.list_of_files[1].columns[4:]
            st.session_state.columnsoffetched=st.session_state.columnsoffetched[:-4]
            st.session_state.columnsofuploaded =st.session_state.list_of_files[0].columns[4:]
            st.session_state.columnsofuploaded = st.session_state.columnsofuploaded [:-4]
            st.session_state.columnsoffetched=[c for c  in st.session_state.columnsoffetched if 'External' not in c and 'Internal' not in c and 'Total' not in c]
            st.session_state.columnsofuploaded =[c for c in  st.session_state.columnsofuploaded  if 'External' not in c and 'Internal' not in c and 'Total' not in c and '.1' not in c and '.2' not in c]
            print("colummmmmmm",st.session_state.columnsoffetched)    
print("enddd",st.session_state.list_of_files)                    
                    
                    
                    
                 
                    
                                 
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
    st.markdown("<h4 style=' color: white;'>Uploaded Data</h4>", unsafe_allow_html=True)
    
    option2 = st.selectbox(
    "Selected the subject(s):", st.session_state.columnsofuploaded 
    )
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
            print("list_updatedafter",list_updated)
            
            

style = "<style>.row-widget.stButton {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)

if st.button("Compare Now!"):
        if len(st.session_state.all_subjects1)!= len(st.session_state.all_subjects2):
            st.error("Please select 2 subjects to compare")
        else:
            
            print("hii")

            dfofone={}
            dfoftwo={}
            for subj1 in st.session_state.all_subjects1:
                print("the data from df is ",st.session_state.list_of_files[1])
                #fetch index of subj1
                index=st.session_state.list_of_files[1].columns.get_loc(subj1)
                
                dfofone[subj1]=list(st.session_state.list_of_files[1].iloc[:,index+2][1:])

            for subj2 in st.session_state.all_subjects2:
                index2=st.session_state.list_of_files[0].columns.get_loc(subj2)
                dfoftwo[subj2]=list(st.session_state.list_of_files[0].iloc[:,index2+2][1:])

            print("dfofone",dfofone)
            print("dfoftwo",dfoftwo)
            dfofone=pd.DataFrame(dfofone)
            dfoftwo=pd.DataFrame(dfoftwo)
            #plotting each subject against the other 
            no_of_graphs=dfofone.shape[1]
            print("no_of_graphs",no_of_graphs)
            for i in range(no_of_graphs):
                subj1 = dfofone.columns[i]
                subj2 = dfoftwo.columns[i]
                print("subj1", subj1)
                print("subj2", subj2)
                y1 = pd.to_numeric(dfofone.iloc[:, i],errors="coerce").sort_values(ascending=True).reset_index(drop=True)
                y2 = pd.to_numeric(dfoftwo.iloc[:, i],errors="coerce").sort_values(ascending=True).reset_index(drop=True)
                print("y1", y1)
                print("y2", y2)
                x = list(range(1, max(len(y1), len(y2)) + 1))
                print("x", x)

                # Adjusting the length of y1 and y2 to match x
                y1 = y1.reindex(range(len(x)))
                y2 = y2.reindex(range(len(x)))
                df=pd.DataFrame({"students":x,subj1:y1,subj2:y2})
                print("df",df)
                df_melted=pd.melt(df,id_vars="students",value_vars=[subj1,subj2],var_name="subjects",value_name="marks")
                print("df_melted",df_melted)
                fig=px.line(df_melted,x="students",y="marks",color="subjects",title=f"Comparison of {dfofone.columns[i]} and {dfoftwo.columns[i]}")
                

            # Display the figure using streamlit
                with st.container():
                    st.plotly_chart(fig)
                    print("plotted")
                    
                    
                    
            #-------------------------Stacked grouped bar chart starts here


            # Create dummy data indexed by state and with multi-columns [product, revenue]
            # index = ["California", "Texas", "Arizona", "Nevada", "Louisiana"]
            selected_subjects1 = st.session_state.all_subjects1
            selected_subjects2 = st.session_state.all_subjects2
            index = [f"{selected_subjects1[i]} and {selected_subjects2[i]}" for i in range(len(selected_subjects1))]

            print("selected_subjects",index)
            df = pd.concat(
                [
                    pd.DataFrame(
                        np.random.rand(2, 2) * 1.25 + 0.25,
                        index=index,
                        columns=["Internal", "External"]
                    ),
                    pd.DataFrame(
                        np.random.rand(2, 2) + 0.5,
                        index=index,
                        columns=["Internal", "External"]
                    ),
                ],
                axis=1,
                keys=["Subject 1", "Subject 2"]
            )

            # Create a figure with the right layout
            fig = go.Figure(
                layout=go.Layout(
                    height=600,
                    width=1000,
                    barmode="relative",
                    yaxis_showticklabels=False,
                    yaxis_showgrid=False,
                    yaxis_range=[0, df.groupby(axis=1, level=0).sum().max().max() * 1.5],
                # Secondary y-axis overlayed on the primary one and not visible
                    yaxis2=go.layout.YAxis(
                        visible=False,
                        matches="y",
                        overlaying="y",
                        anchor="x",
                    ),
                    font=dict(size=24),
                    legend_x=0,
                    legend_y=1,
                    legend_orientation="h",
                    hovermode="x",
                    margin=dict(b=0, t=10, l=0, r=10)
                )
            )

            # Define some colors for the product, revenue pairs
            colors = {
                "Subject 1": {
                    "Internal": "#F28F1D",
                    "External": "#F6C619",
                },
                "Subject 2": {
                    "Internal": "#2B6045",
                    "External": "#5EB88A",
                }
            }

            # Add the traces
            for i, t in enumerate(colors):
                for j, col in enumerate(df[t].columns):
                    if (df[t][col] == 0).all():
                        continue
                    fig.add_bar(
                        x=df.index,
                        y=df[t][col],
                        # Set the right yaxis depending on the selected product (from enumerate)
                        yaxis=f"y{i + 1}",
                        # Offset the bar trace, offset needs to match the width
                        # For categorical traces, each category is spaced by 1
                        offsetgroup=str(i),
                        offset=(i - 1) * 1/3,
                        width=1/3,
                        legendgroup=t,
                        legendgrouptitle_text=t,
                        name=col,
                        marker_color=colors[t][col],
                        marker_line=dict(width=2, color="#333"),
                        hovertemplate="%{y}<extra></extra>"
                    )

            # Display the plot in Streamlit
            st.plotly_chart(fig)

            #------------------------------------stacked grouped bar chart ends here                    
                    
                    
                    

                
    

    