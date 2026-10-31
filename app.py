import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities

# Page setup
st.set_page_config(
    page_title="CampusGraph",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 CampusGraph")
st.subheader("Student Network & Collaboration Analyzer")

st.write(
    "CampusGraph analyzes student connections, skills and collaborations "
    "using NetworkX and Pandas."
)

# Load datasets
students = pd.read_csv("data/students.csv")
skills = pd.read_csv("data/skills.csv")
interactions = pd.read_csv("data/interactions.csv")

# Build graph
G = nx.Graph()

for student_id in students["student_id"]:
    G.add_node(student_id)

for _, row in interactions.iterrows():
    G.add_edge(
        row["student1"],
        row["student2"],
        interaction=row["interaction_type"]
    )

# Student information
student_names = dict(
    zip(students["student_id"], students["name"])
)

degree = dict(G.degree())
degree_centrality = nx.degree_centrality(G)

student_skills = (
    skills.groupby("student_id")["skill"]
    .apply(set)
    .to_dict()
)

# Communities
communities = list(greedy_modularity_communities(G))

# Dashboard statistics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Students", G.number_of_nodes())
col2.metric("Connections", G.number_of_edges())
col3.metric("Communities", len(communities))
col4.metric("Isolated Students", len(list(nx.isolates(G))))

# Student analysis
st.header("Student Analysis")

selected_student = st.selectbox(
    "Select a student",
    students["student_id"],
    format_func=lambda x: f"{student_names[x]} ({x})"
)

st.write("**Selected student:**", student_names[selected_student])
st.write("**Number of connections:**", degree[selected_student])
st.write(
    "**Degree centrality:**",
    round(degree_centrality[selected_student], 3)
)

# Skills
st.subheader("Student Skills")

selected_skills = student_skills.get(selected_student, set())

st.write(", ".join(sorted(selected_skills)))

# Collaborator recommendations
st.subheader("Recommended New Collaborators")

recommendations = []

for other_id, other_skills in student_skills.items():

    if other_id == selected_student:
        continue

    if G.has_edge(selected_student, other_id):
        continue

    common_skills = selected_skills & other_skills
    score = len(common_skills)

    if score > 0:
        recommendations.append(
            (other_id, score, common_skills)
        )

recommendations.sort(
    key=lambda x: x[1],
    reverse=True
)

if recommendations:

    for student_id, score, common_skills in recommendations[:5]:

        st.write(
            f"**{student_names[student_id]} ({student_id})**"
        )

        st.write(
            f"Shared skills: {', '.join(sorted(common_skills))}"
        )

        st.write(
            f"Compatibility score: {score}"
        )

        st.divider()

else:
    st.write("No new collaborators found.")

# Network visualization
st.header("Student Network")

fig, ax = plt.subplots(figsize=(10, 7))

pos = nx.spring_layout(G, seed=42)

node_sizes = [
    degree[student] * 300
    for student in G.nodes()
]

nx.draw(
    G,
    pos,
    ax=ax,
    with_labels=True,
    node_size=node_sizes,
    font_size=9
)

ax.set_title("Campus Student Network")

st.pyplot(fig)