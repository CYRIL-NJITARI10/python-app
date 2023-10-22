import streamlit as st
import requests

def main():
    st.title("Google Cookies Viewer")

    if st.button("Fetch Google Cookies"):
        response = requests.get("http://localhost:8080/make_google_request")
        if response.status_code == 200:
            cookies_str = response.text
            st.markdown("### Cookies from Google:")
            st.text(cookies_str)  # Displaying the cookies string directly
        else:
            st.error("Failed to fetch cookies. Ensure Flask app is running.")
    if st.button("Fetch Google Analytics Data"):
        response = requests.get("http://localhost:8080/make_ganalytics_request")
        if response.status_code == 200:
            html_content = response.text
            st.markdown("### Google Analytics Data:")
            st.write(html_content)
        else:
            st.error("Failed to fetch Google Analytics data. Ensure Flask app is running.")
    if st.button("Fetch Google Analytics Data"):
        response = requests.get("http://localhost:8080/make_ganalytics_request")
        if response.status_code == 200:
            ganalytics_data = response.json()

            st.markdown("### Google Analytics Data:")
            
            # Display the status code
            st.text(ganalytics_data['status_code'])
            
            # Display the response text
            st.markdown(ganalytics_data['text'])
        else:
            st.error("Failed to fetch Google Analytics data. Ensure Flask app is running.")

if __name__ == '__main__':
    main()




    import os

@app.route('/oauth2callback')
def oauth2callback():
    try:
        # Étape 1: Authentifiez-vous avec OAuth 2.0
        SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        
        # Utilisez une variable d'environnement pour votre fichier de credentials
        creds_file_path = os.getenv('GOOGLE_CREDS_FILE', 'credentials.json')
        
        flow = InstalledAppFlow.from_client_secrets_file(creds_file_path, SCOPES)

        flow.redirect_uri = "http://localhost:8080/oauth2callback"

        redirect_uri = flow.redirect_uri
        app.logger.info(f"Using redirect URI: {redirect_uri}")
        
        creds = flow.run_local_server(port=8080, host='localhost', 
                                      authorization_prompt_message='good', 
                                      success_message='success', 
                                      open_browser=True)
        
        # Étape 2: Construisez le service Google Analytics
        service = build('analytics', 'v3', credentials=creds)

        # Utilisez une variable d'environnement pour le profile_id
        profile_id = os.getenv('GA_PROFILE_ID', '408224738')
        
        results = service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='30daysAgo',
            end_date='today',  
            metrics='ga:visitors').execute()

        visitors = results.get('rows')[0][0]
        
        return f"Nombre de visiteurs: {visitors}"
    except Exception as e:
        app.logger.error(f"Error fetching visitors count: {str(e)}")
        return "Erreur lors de la récupération du nombre de visiteurs.", 500
