********CampusGraph********

Student Network and Collaboration Analyzer

CampusGraph is a Python-based application that models student relationships as a network and analyzes connections, communities, skills, and potential collaboration opportunities.

Features
Student network visualization using NetworkX
Degree and degree-centrality analysis
Community detection
Shortest-path analysis
Identification of isolated students
Skill-based collaborator recommendations
SQLite database integration
Interactive Streamlit dashboard
Technologies Used
Python
Pandas
NetworkX
Matplotlib
SQLite
Streamlit
Dataset

The project uses a synthetic/anonymized campus dataset containing information about:

Students
Skills
Courses
Projects
Student-project relationships
Student interactions
How to Run

Install the required Python libraries:

pip install -r requirements.txt

Run the Streamlit application:

python -m streamlit run app.py

The application will open in the browser at the local Streamlit address.

Project Structure
CampusGraph/
├── data/
│   ├── students.csv
│   ├── skills.csv
│   ├── courses.csv
│   ├── projects.csv
│   ├── student_projects.csv
│   └── interactions.csv
├── CampusGraph.ipynb
├── app.py
├── campus.db
├── requirements.txt
└── README.md
