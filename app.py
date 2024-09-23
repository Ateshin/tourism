import pandas as pd
import streamlit as st
import plotly.express as px
df = pd.read_csv("C:\\Users\\Hussein\\Desktop\\Tourism.csv")
df = df.drop(labels=[
    "Existence of hotels - does not exist", 
    "Existence of cafes - does not exist", 
    "Existence of touristic attractions that can be expolited and developed - does not exist",
    "Existence of restaurants - does not exist", 
    "Existence of hotels - exists", 
    "Existence of restaurants - exists", 
    "publisher", 
    "Observation URI", 
    "Existence of guest houses - exists", 
    "dataset", 
    "references", 
    "Existence of cafes - exists", 
    "Existence of guest houses - does not exist"
], axis=1)
df['refArea'] = df['refArea'].str.split('/').str[-1]
df['refArea'] = df['refArea'].replace("Miniyehâ\x80\x93Danniyeh_District", "Danniyeh_District")
df['refArea'] = df['refArea'].replace("ZahlÃ©_District", "Zahle_District")
df['refArea'] = df['refArea'].replace("Tripoli_District,_Lebanon", "Tripoli_District")
df['refArea'] = df['refArea'].str.replace(r'(_Governorate|_District)', '', regex=True).str.replace('_', ' ')
df.columns = ['Nb of Restaurants', 'Town', 'Area', 'Potential Touristic Attractions for Development', 'Nb of Guest Houses', 'Nb of Hotels', 'Tourism Projects - Past 5 Years', 'Nb of Cafes', 'Tourism Index']
st.title("Tourism Data Visualization")
# Sidebar Filters
selected_areas = st.sidebar.multiselect(
    'Select Areas to Display:',
    options=df['Area'].unique(),
    default=df['Area'].unique()
)

# Slider to Filter by Tourism Index
min_index, max_index = int(df['Tourism Index'].min()), int(df['Tourism Index'].max())
selected_index = st.sidebar.slider(
    'Select Tourism Index Range:',
    min_value=min_index,
    max_value=max_index,
    value=(min_index, max_index)
)

# Ensure that filtered_df is defined correctly
filtered_df = df[(df['Area'].isin(selected_areas)) & 
                 (df['Tourism Index'] >= selected_index[0]) & 
                 (df['Tourism Index'] <= selected_index[1])]

# Sidebar selection
option = st.sidebar.selectbox(
    'Select a visualization type:',
    ['Total Number of Restaurants by Area', 'Total Number of Guest Houses by Area',
     'Total Number of Hotels by Area', 'Total Number of Cafes by Area', 'Distribution of Tourism Index',
     'Stacked Comparison of Hospitality Services by Area', 'Comparison of Touristic Attractions and Tourism Projects']
)

# Visualizations with Descriptions
if option == 'Total Number of Restaurants by Area':
    df_grouped = filtered_df.groupby('Area').sum().reset_index()
    fig = px.bar(df_grouped, x='Area', y='Nb of Restaurants', title='Total Number of Restaurants by Area')
    st.plotly_chart(fig)
    st.write("**Observation:** This visualization shows the total number of restaurants available in each area, highlighting areas with more developed restaurant services.")

elif option == 'Total Number of Guest Houses by Area':
    df_grouped = filtered_df.groupby('Area').sum().reset_index()
    fig = px.bar(df_grouped, x='Area', y='Nb of Guest Houses', title='Total Number of Guest Houses by Area')
    st.plotly_chart(fig)
    st.write("**Observation:** This chart highlights the distribution of guest houses across different areas, indicating which regions have more developed accommodations.")

elif option == 'Total Number of Hotels by Area':
    df_grouped = filtered_df.groupby('Area').sum().reset_index()
    fig = px.bar(df_grouped, x='Area', y='Nb of Hotels', title='Total Number of Hotels by Area')
    st.plotly_chart(fig)
    st.write("**Observation:** The visualization depicts the number of hotels in each area, which can be an indicator of tourism infrastructure development.")

elif option == 'Total Number of Cafes by Area':
    df_grouped = filtered_df.groupby('Area').sum().reset_index()
    fig = px.bar(df_grouped, x='Area', y='Nb of Cafes', title='Total Number of Cafes by Area')
    st.plotly_chart(fig)
    st.write("**Observation:** This chart illustrates the distribution of cafes, showcasing areas with more vibrant café cultures.")

elif option == 'Distribution of Tourism Index':
    fig = px.pie(filtered_df, names='Tourism Index', title='Distribution of Tourism Index', hole=0.3)
    st.plotly_chart(fig)
    st.write("**Observation:** This pie chart provides insights into the overall distribution of the tourism index, reflecting the varying levels of tourism development.")

elif option == 'Stacked Comparison of Hospitality Services by Area':
    df_melted = filtered_df.melt(id_vars='Area', value_vars=['Nb of Restaurants', 'Nb of Hotels', 'Nb of Cafes', 'Nb of Guest Houses'],
                                 var_name='Category', value_name='Count')
    fig = px.bar(df_melted, x='Area', y='Count', color='Category', barmode='stack',
                 title='Stacked Comparison of Hotels, Cafes, Guest Houses, and Restaurants by Area')
    st.plotly_chart(fig)
    st.write("**Observation:** This stacked bar chart compares the various hospitality services in each area, showing the combined presence of hotels, cafes, guest houses, and restaurants.")

elif option == 'Comparison of Touristic Attractions and Tourism Projects':
    df_melted = filtered_df.melt(id_vars='Area', value_vars=['Potential Touristic Attractions for Development', 'Tourism Projects - Past 5 Years'],
                                 var_name='Category', value_name='Count')
    fig = px.bar(df_melted, x='Area', y='Count', color='Category', barmode='group',
                 title='Comparison of Potential Touristic Attractions and Tourism Projects by Area')
    st.plotly_chart(fig)
    st.write("**Observation:** This chart compares the number of potential touristic attractions against recent tourism projects, offering insights into areas with growth opportunities.")