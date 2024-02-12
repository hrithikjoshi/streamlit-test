# streamlit_app.py

import streamlit as st
import tableauserverclient as TSC


# Set up connection.

st.markdown("### Earthquake Dashboard ###")

tableau_auth = TSC.PersonalAccessTokenAuth(
    st.secrets["tableau"]["token_name"],
    st.secrets["tableau"]["personal_access_token"],
    st.secrets["tableau"]["site_id"],
)
server = TSC.Server(st.secrets["tableau"]["server_url"], use_server_version=True)


# Get various data.

@st.experimental_memo(ttl=1200)
def run_query(view_name):
    with server.auth.sign_in(tableau_auth):

        # Get all workbooks.
        workbooks, pagination_item = server.workbooks.get()
        for w in workbooks:
            if w.name == 'Account Engagement':
                our_workbook = w
                break

        # Get views for ABC workbook.
        server.workbooks.populate_views(our_workbook)
        for v in our_workbook.views:
            if view_name == v.name:
                our_view = v
                break

        # Get image of the view
        server.views.populate_image(our_view)
        view_image = our_view.image
        
        return view_image
    
view_image = run_query("Account Engagement")
st.image(view_image, width=800)