@echo off

cd /d %~dp0

echo Activating conda environment...

call C:\Users\palex\anaconda3\Scripts\activate.bat STREAMLIT_Shiny

echo Starting Streamlit app...

streamlit run habitat_map_validation-master.py

pause