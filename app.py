import streamlit as st
import json
import random

# Topics configuration
TOPICS = {
    "01 Introduction to Python": "01_introduction_to_python.json",
    "02 Data Types": "02_data_types.json",
    "03 Operators & Variables": "03_operators_keywords_variables.json",
    "04 Strings & Casting": "04_strings_casting.json",
    "05 Control Flow": "05_control_flow.json",
    "06 Lists/Tuples/Dicts": "06_lists_tuples_dict.json",
    "07 Sets": "07_sets.json",
    "08 Modules & Functions": "08_modules_functions.json",
    "09 Exception Handling": "09_exception_handling.json",
    "10 File Handling": "10_file_handling.json",
    "11 Math & Datetime": "11_math_datetime.json",
    "12 OOP Part 1": "12_oop_part_1.json",
    "13 OOP Part 2": "13_oop_part_2.json",
    "14 Async & Threading": "14_asyncio_threading.json",
    "15 CPython & GIL": "15_cpython_gil.json",
}

# Session State Initialization
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}


# Load questions
def load_questions(topic_file):
    try:
        with open(topic_file, "r") as f:
            return json.load(f)["questions"]
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return []


# App Layout
st.title("Python MCQ Quiz System")
st.markdown("### Test your Python knowledge!")

# Sidebar
with st.sidebar:
    st.header("Topics")
    selected_topic = st.selectbox("Choose a topic:", options=list(TOPICS.keys()))

    if st.button("Start Quiz"):
        st.session_state.current_topic = TOPICS[selected_topic]
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.user_answers = {}
        st.session_state.show_explanation = False
        st.rerun()

# Quiz Logic
if st.session_state.current_topic:
    questions = load_questions(st.session_state.current_topic)

    if questions:
        total_questions = len(questions)
        progress = st.session_state.current_question / total_questions

        st.header(f"{selected_topic} Quiz")
        st.markdown(
            f"**Progress:** {st.session_state.current_question + 1}/{total_questions}"
        )
        st.progress(progress)

        question = questions[st.session_state.current_question]

        with st.form("question_form"):
            st.subheader(question["question"])
            user_answer = st.radio(
                "Select your answer:", question["options"], index=None
            )

            submitted = st.form_submit_button("Submit")

            if submitted and user_answer:
                st.session_state.user_answers[st.session_state.current_question] = (
                    user_answer
                )
                st.session_state.show_explanation = True

                if user_answer == question["options"][question["correct_answer"]]:
                    st.success("Correct!")
                    st.session_state.score += 1
                else:
                    st.error("Incorrect")

                with st.expander("Explanation"):
                    st.markdown(
                        f"**Correct Answer:** {question['options'][question['correct_answer']]}"
                    )
                    st.markdown(question["explanation"])

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.session_state.current_question > 0:
                if st.button("Previous"):
                    st.session_state.current_question -= 1
                    st.session_state.show_explanation = False
                    st.rerun()
        with col3:
            if st.session_state.current_question < total_questions - 1:
                if st.button("Next"):
                    st.session_state.current_question += 1
                    st.session_state.show_explanation = False
                    st.rerun()
            else:
                if st.button("Finish"):
                    st.success(
                        f"Quiz Complete! Final Score: {st.session_state.score}/{total_questions}"
                    )
                    if st.button("Restart"):
                        st.session_state.current_question = 0
                        st.session_state.score = 0
                        st.session_state.user_answers = {}
                        st.session_state.show_explanation = False
                        st.rerun()

# Initial State
else:
    st.markdown(
        """
    ## Welcome to Python Quiz Master!
    
    ### Features:
    - 15+ Python Topics
    - Interactive MCQ System
    - Detailed Explanations
    - Progress Tracking
    
    ### How to Start:
    1. Select a topic from the sidebar
    2. Click 'Start Quiz'
    3. Answer questions and learn!
    """
    )
