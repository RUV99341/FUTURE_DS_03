import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup
st.set_page_config(layout="wide", page_icon="📊", page_title="Student Feedback Dashboard")
st.title("🎓 Student Feedback Analysis")
st.markdown("""
This dashboard presents a comprehensive analysis of student satisfaction based on course feedback.
All visualizations are designed for clarity and impact.
""")

# Load data
df = pd.read_csv("data/Student_Satisfaction_Survey.csv", encoding='ISO-8859-1')
df[['Rating', 'Percent']] = df['Average/ Percentage'].str.split('/', expand=True).astype(float)
df['Avg_Rating_Text'] = df['Rating']

# --- Layout ---
st.sidebar.header("📌 Navigation")
section = st.sidebar.radio("Go to Section:", [
    "Overview",
    "Top Rated Courses",
    "Lowest Rated Questions",
    "Weak Areas",
    "Satisfaction by Stream",
    "Feedback Submission Stats",
    "Rating vs Participation",
    "Course-Question Heatmap"
])

# --- Visualizations ---

if section == "Overview":
    st.subheader("🔍 Rating Distribution Across Courses")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df['Avg_Rating_Text'], bins=10, kde=True, color='teal', ax=ax)
    ax.set_title("Overall Rating Distribution", fontsize=14)
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

elif section == "Top Rated Courses":
    st.subheader("🌟 Top 10 Highest Rated Courses")
    top_courses = df.groupby('Course Name ')['Avg_Rating_Text'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_courses.values, y=top_courses.index, palette="viridis", ax=ax)
    ax.set_title("Top 10 Courses by Student Rating", fontsize=14)
    ax.set_xlabel("Average Rating")
    ax.set_xlim(0, 5)
    st.pyplot(fig)

elif section == "Lowest Rated Questions":
    st.subheader("🚨 Bottom 10 Feedback Questions")
    question_avg = df.groupby('Questions')['Avg_Rating_Text'].mean().sort_values().head(10)
    fig, ax = plt.subplots(figsize=(10, 9))
    sns.barplot(x=question_avg.values, y=question_avg.index, palette="rocket", ax=ax)
    ax.set_title("Lowest Rated Questions", fontsize=14)
    ax.set_xlabel("Average Rating")
    ax.set_xlim(0, 5)
    st.pyplot(fig)

elif section == "Weak Areas":
    st.subheader("📉 Areas for Improvement in Teaching & Learning")

    # Calculate lowest-rated questions
    weak_questions = df.groupby('Questions')['Avg_Rating_Text'].mean().sort_values().head(10)

    st.markdown("These feedback questions consistently received the lowest average scores. Addressing them may improve overall student satisfaction.")

    # Display table
    st.table(
        weak_questions.reset_index().rename(
            columns={"Questions": "Feedback Question", "Avg_Rating_Text": "Average Rating"}
        )
    )

    # Bar chart
    fig, ax = plt.subplots(figsize=(10, 9))
    sns.barplot(
        x=weak_questions.values,
        y=weak_questions.index,
        palette="Reds_r",
        ax=ax
    )
    ax.set_title("🔻 Bottom 10 Rated Feedback Questions", fontsize=14)
    ax.set_xlabel("Average Rating", fontsize=12)
    ax.set_ylabel("Feedback Question", fontsize=12)
    ax.set_xlim(0, 5)
    st.pyplot(fig)



elif section == "Satisfaction by Stream":
    st.subheader("📚 Satisfaction by Degree Stream")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='Basic Course', y='Avg_Rating_Text', palette="Set2", ax=ax)
    ax.set_title("Rating Distribution Across Streams", fontsize=14)
    ax.set_xlabel("Stream")
    ax.set_ylabel("Average Rating")
    plt.setp(ax.get_xticklabels(), rotation=60)
    st.pyplot(fig)

elif section == "Feedback Submission Stats":
    st.subheader("🧾 Feedback Submission Count by Course")
    submission_counts = df['Course Name '].value_counts().head(15)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=submission_counts.values, y=submission_counts.index, palette="coolwarm", ax=ax)
    ax.set_title("Top 15 Courses by Feedback Count", fontsize=14)
    ax.set_xlabel("Submission Count")
    ax.set_ylabel("Course Name")
    ax.set_xticks(range(0, 45, 5))  # X-axis ticks: 0, 5, 10, ..., 40
    st.pyplot(fig)

elif section == "Rating vs Participation":
    st.subheader("📈 Ratings vs Feedback Participation")
    grouped = df.groupby('Course Name ').agg({
        'Avg_Rating_Text': 'mean',
        'SN': 'count'
    }).rename(columns={'SN': 'Feedback Count'})
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=grouped, x='Feedback Count', y='Avg_Rating_Text', s=70, color='mediumseagreen', ax=ax)
    ax.set_title("Do More Ratings Mean Better Scores?", fontsize=14)
    ax.set_xlabel("Number of Feedback Submissions")
    ax.set_ylabel("Average Course Rating")
    st.pyplot(fig)

elif section == "Course-Question Heatmap":
    st.subheader("🌐 Heatmap of Ratings by Course & Question")
    pivot = df.pivot_table(index='Course Name ', columns='SN', values='Avg_Rating_Text', aggfunc='mean')
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(pivot, cmap='YlGnBu', linewidths=0.5, linecolor='gray', ax=ax)
    ax.set_title("Average Ratings per Question per Course", fontsize=14)
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit | Data: Student Feedback Survey")
