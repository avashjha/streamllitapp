import streamlit as st
from pivottablejs import pivot_ui
import pandas as pd  
from PIL import Image
from datetime import datetime,date
import random
import altair as alt
import streamlit.components.v1 as components
import os
import os.path
import time
import re


#upload file
#ufile=st.sidebar.file_uploader('Upload',type=['csv','txt','xls','xlsx'])

#load data from url
@st.cache
def load_data():
    url='https://0e0c55ie39.execute-api.eu-central-1.amazonaws.com/default/fplAnalytics-DownloadPlayerStatusData'
    data=pd.read_csv(url)
    return data

def fpl():
    data=load_data()
    df=data

  
    if st.checkbox('Team'):
        
        steam=st.selectbox('select team',df.team.unique())
        st.table(df[(df.team==steam)])

    if st.checkbox('player status'):
        status=st.selectbox('Select status',df.status.unique())
        opt=st.multiselect('select parameter',df.columns.to_list())
        st.write(df[opt][df.status==status])

    if st.checkbox('visualize performance in table'):
        choice=st.selectbox('Choices',['bestandworst','topten','mvp','fpll'])

        if choice=='bestandworst':
            best_tp=df.total_points.max()
            worst_tp=df.total_points.min()
            bonus_max=df.bonus.max()
            choice=['name','team','position','total_points','bonus']
            rad=st.radio('options',['min','max','bonus'])
            if rad=='max':

                st.table(df[choice][(df.total_points==best_tp)])
            elif rad=='min':
                st.table(df[choice][(df.total_points==worst_tp)])
            elif rad=='bonus':
                st.write('highest bonus')
                st.table(df[choice][(df.bonus==bonus_max)])
    
        if choice=='topten':
            criteria=df.sort_values(by='points_per_game')
            st.write('TOP 10 Players by MVP ')
            st.table(criteria[-10:])

            if st.button('Generate chart'):
                cust_data=criteria[-10:]
                chart_data=pd.DataFrame(cust_data)
                #pie_plot=chart_data.value_counts().plot.pie()
                #st.write(pie_plot)
                cdata=alt.Chart(chart_data).mark_circle(interpolate='basis').encode(
                    alt.X('name',title="player's name "),
                    alt.Y('total_points',title='performance (based on total_points'),
                    color='team:N',
                    size='bonus:N'
                ).properties(title='Data in chart format')

                st.altair_chart(cdata,use_container_width=True)
            

        if choice=='mvp':

            criteria=df.sort_values(by='selected_by_percent')
            st.write('Top 10 palyers choosen by people ')
            st.table(criteria[-10:])

            if st.button('Generate chart'):
                cust_data=criteria[-10:]
                chart_data=pd.DataFrame(cust_data)
                #pie_plot=chart_data.value_counts().plot.pie()
                #st.write(pie_plot)
                cdata=alt.Chart(chart_data).mark_circle(interpolate='basis').encode(
                    alt.X('name',title="player's name "),
                    alt.Y('total_points',title='performance (based on total_points'),
                    color='team:N',
                    size='bonus:N'
                ).properties(title='Data in chart format')

                st.altair_chart(cdata,use_container_width=True)
                

        if choice=='fpll':
            st.write('fpl points leader board (top 4 players are shown of each team)')
            
            group=df.groupby('team')
            for i,j in group:
                tp=j.sort_values(by='total_points')
                sl=tp[-4:]
            # tpsum=sl.total_points.sum()
                #sl.apply(lambda x: x.append(x.aggregate(dict(mean_index='mean',sum_index='sum'))))
                
                st.write(i)
                st.table(sl)      


def anal():
    #file_uploader command from streamlit
    anal=st.file_uploader('Choose a file',type=['csv'])
    if anal is not None:
        #to eradicate errors    
        anal.seek(0)
        df=pd.read_csv(anal,low_memory=False)
      

        
        st.write('Some data are:')
        st.dataframe(df.head(5)) 
        if st.checkbox('Show in groups'):
            columnss=st.selectbox('columns in the file are:',df.columns)
            if st.button('Generate by columns'):
                g=df.groupby(columnss)
                for i,j in g:
                    st.title(f"{i}")
                    st.table(j)
            if st.button('Save file in xls format'):
                g=df.groupby(columnss)
                #today=date.today()
                #foldername=datetime.strftime(today,"%Y-%m-%d %H:%M")
                #os.mkdir(f"{foldername}")
                for i,j in g:
                    j.to_excel(f"{i}.xls",index=False)
                st.success('file saved successfully....')
        if st.checkbox('search email from a file'):
            col_search=df.columns
            for email in col_search:
                if 'email' in email:
                    email_col=email
                    email_id=df[email_col]
                    receiver=email_id
                    st.write(receiver)
                
            st.warning('no email found in the file, Sorry :(')

        
def nepse():
    data=st.file_uploader('Choose a file',type=['csv'])
    if data is not None:
        #to eradicate errors    
        data.seek(0)
        df=pd.read_csv(data,low_memory=False)
        st.dataframe(df.head(5))

        if st.checkbox('Analyze the data'):
            df.columns=df.columns
            df.columns=df.columns.str.replace('.','')
            df.columns=df.columns.str.replace(' ','_')
            
            #st.write(df.columns)

            #st.write(df.info())
            choice=st.selectbox('see details by',['top_ten','top_looser'])
            if choice=='top_ten':
                selectchoice=st.selectbox('choose by ', df.columns[1:])

                top_ten=df.sort_values(by=selectchoice,ascending=False)[:10]
                st.table(top_ten)

                if st.button('in Chart'):
                    st.empty()
                    chart_data=alt.Chart(top_ten).mark_bar(interpolate='basis').encode(
                        alt.X('Traded_Companies'),
                        alt.Y(selectchoice),
                        color='Traded_Companies',
                        size=f"{selectchoice}:N")
                    
                    st.altair_chart(chart_data,use_container_width=True)
                
                  

            elif choice=='top_looser':
                selectchoice=st.selectbox('choose by ', df.columns[1:])

                top_looser=df.sort_values(by=selectchoice,ascending=True)[:10]
                st.table(top_looser)

                if st.button('in Chart'):
                    brush = alt.selection_interval()             
                    chart_data=alt.Chart(top_looser).mark_circle().encode(
                        alt.X('Traded_Companies'),
                        alt.Y(f"{selectchoice}"),
                        color='Traded_Companies:N',
                        size=f"{selectchoice}:Q"
                    ).add_selection(
                        brush
                        )
                             
                    st.altair_chart(chart_data,use_container_width=True)

                
        if st.checkbox('Pivotize'):
            df.columns=df.columns
            df.columns=df.columns.str.replace('.','')
            df.columns=df.columns.str.replace(' ','_')

            t=pivot_ui(df)
            with open(t.src) as t:
                components.html(t.read(), width=900, height=1000, scrolling=True)
                
                




                
                
def main():
      
    #menu in sidebar
    #st.sidebar.title("Menu")
    #menu choice in list
    choice=st.sidebar.selectbox('Menu',['FPL','Explore','Nepse','Image to Pdf','About'])

    if choice=='FPL':
        st.title('FPL analysis')
       
        st.subheader('relying on data from fplanalytics.com')
        st.sidebar.markdown('''
        * Latest GameWeek points of English Premier League are shown.
        * If you have any suggestion or words reach out the about section.
                ''')
        fpl()
    elif choice=='Explore':
        st.title('Explore csv file and convert it into specific options as below:')  
        st.sidebar.markdown('''
        * Note: If the file is in xls format please change to csv file and upload it
        * check video to see how you can convert the excel file to csv format [youtube_link](https://youtu.be/QBN0M0Vxayc)
                ''')
        anal()

    elif choice=='Nepse':
        st.title('upload csv file of nepse to explore data')
        st.sidebar.markdown('''
        * Note: If the file is in xls format please change to csv file and upload it
        * check video to see how you can convert the excel file to csv format [youtube_link](https://youtu.be/QBN0M0Vxayc)
        * only works with data taken from [http://www.nepalstock.com/todaysprice](http://www.nepalstock.com/todaysprice).
        
        
                ''')
        
        nepse()
    
    elif choice=='Image to Pdf':
        st.title('Convert image to pdf')
        file_upload=st.file_uploader('Upload',type=['jpg','jpeg','png'])
        
        if file_upload is not None:
           
           if st.button('Save'):

               im1 = Image.open(file_upload).convert("RGB")
                #im2 = PIL.Image.open("2.jpg").convert("RGB")
                #im3 = PIL.Image.open("3.jpg").convert("RGB")
               images = [im1]
               #st.download_button(label="Download image",data=images,file_name=f"{images}",mime="image/pdf",)
               path=os.getcwd()
               #im1.save(f"{path}/out.pdf", save_all=True, append_images=images)
               #st.info(f'file converted sucessfully to {path}')
               with save(f"{path}/out.pdf", "rb") as file:
                   btn = st.download_button(
                        label="Download image",
                        data=file,
                        file_name=f"random.pdf",
                        mime="image/pdf",
                    )
                         
               


        
        
        
    elif choice=='About':
        html_p="""
                                <!DOCTYPE html>
                <html>
                <body>

                <p>If you have any query message him .... </p>

                <form action="mailto:avashjhaymail@gmail.com" method="post" enctype="text/plain">
                Name:<br>
                <input type="text" name="name"><br>
                E-mail:<br>
                <input type="text" name="mail"><br>
                Comment:<br>
                <input type="text" name="comment" size="100"><br><br>
                <input type="submit" value="Send">
                <input type="reset" value="Reset">
                </form>

               
                </body>
                </html>


        """
               
        st.sidebar.markdown("""
        # App developed by Avash
        ## Note
        - use for personal use.
        - this app is developed for personal project and is currently in beta version.
        - if you want to use it commercial use please contact avash through email.
                        
        """)
        components.html(html_p,height=500,width=500)
        st.info('Made with love from Avash.')





if __name__ == "__main__":
    main()


