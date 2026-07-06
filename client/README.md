# Course Scheduler Client

This Streamlit app is the frontend for the course scheduler server.

## Run the app

1. Start the server:
   ```bash
   cd server
   python main.py
   ```
2. Start the client via Streamlit:
   ```bash
   cd client
   streamlit run app.py
   ```

Alternative on Windows:
   ```bash
   cd client
   python run_client.py
   ```

## Workflow

1. Upload `a.txt`
2. Review the course catalogue
3. Select courses using the buttons
4. Click proceed and provide completed prerequisites
5. View Plan A recommendations and conflict messages
6. Enter weights for each selected course
7. Generate Plan B optimized schedule
