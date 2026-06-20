import streamlit as st

from database.auth import create_user, login_user
from utils.gemini_client import get_gemini_response
from database.stats import add_xp, get_stats


# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="Lumina AI",
    page_icon="🧠",
    layout="wide"
)


# ----------------------------
# SESSION STATE
# ----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "xp" not in st.session_state:
    st.session_state.xp = 120

if "streak" not in st.session_state:
    st.session_state.streak = 5


# ----------------------------
# HEADER
# ----------------------------

st.title("🧠 Lumina AI")
st.subheader("Illuminating the Path to Intelligent Learning")


# ----------------------------
# LOGIN / SIGNUP
# ----------------------------

if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Choose Option",
        ["Login", "Signup"]
    )

    # ----------------------------
    # SIGNUP
    # ----------------------------

    if menu == "Signup":

        st.header("Create Account")

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Signup"):

            success = create_user(
                username,
                password
            )

            if success:
                st.success(
                    "Account created successfully!"
                )

            else:
                st.error(
                    "Username already exists!"
                )

    # ----------------------------
    # LOGIN
    # ----------------------------

    else:

        st.header("Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

            # ==================================================
# MAIN APP AFTER LOGIN
# ==================================================

else:

    st.success(
        f"Welcome back, {st.session_state.username}! 🚀"
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Command Center",
        "💬 Study Engine",
        "🎯 Assessment Zone",
        "🚨 Exam Night"
    ])


        # =====================================
    # TAB 1 : COMMAND CENTER
    # =====================================

    with tab1:

        st.header("🏠 Command Center")

        stats = get_stats(
            st.session_state.username
        )

        if stats:

            xp = stats[0]
            streak = stats[1]
            sessions = stats[2]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "⭐ XP",
                    xp
                )

            with col2:
                st.metric(
                    "🔥 Streak",
                    streak
                )

            with col3:
                st.metric(
                    "📚 Sessions",
                    sessions
                )

        st.subheader(
            f"Welcome, {st.session_state.username} 👋"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                "🔥 Study Streak\n\nWill be calculated from actual activity."
            )

        with col2:
            st.info(
                "⭐ XP\n\nWill be loaded from database."
            )

        st.divider()

        st.subheader("📊 Learning Analytics")

        st.write(
            "Analytics will appear after quizzes and study sessions are stored."
        )

        st.divider()

        st.subheader("🎯 Today's Goal")

        st.write(
            "Complete at least one learning activity inside Lumina."
        )


       # =====================================
    # TAB 2 : STUDY ENGINE
    # =====================================

    with tab2:

        st.header("💬 Study Engine")

        mode = st.radio(
            "Choose Learning Mode",
            [
                "🧠 Deep Dive",
                "🧒 Explain Like I'm 10",
                "📝 Notes Simplifier",
                "🃏 Flashcards"
            ],
            horizontal=True
        )

        user_input = st.text_area(
            "Enter your topic/question"
        )

        if st.button("Generate Response"):

            if mode == "🧠 Deep Dive":

                prompt = f"""
                Explain this topic in detail.

                Include:
                1. Simple Explanation
                2. Detailed Explanation
                3. Real Life Example
                4. Related Topics

                Topic:
                {user_input}
                """

            elif mode == "🧒 Explain Like I'm 10":

                prompt = f"""
                Explain this topic like I am 10 years old.

                Use:
                - Simple language
                - Stories
                - Analogies
                - Hinglish examples

                Topic:
                {user_input}
                """

            elif mode == "📝 Notes Simplifier":

                prompt = f"""
                Convert this into:

                1. Short Notes
                2. Revision Notes
                3. Key Points

                Content:
                {user_input}
                """

            else:

                prompt = f"""
                Create flashcards.

                Format:

                Q:
                A:

                Topic:
                {user_input}
                """

            with st.spinner("Lumina is thinking..."):

                answer = get_gemini_response(prompt)
                add_xp(
    st.session_state.username,
    5
)

            st.write(answer)

                # =====================================
    # TAB 3 : ASSESSMENT ZONE
    # =====================================

    with tab3:

        st.header("🎯 Assessment Zone")

        st.subheader("🎤 Viva Simulator")

        subject = st.text_input(
            "Enter Subject",
            key="viva_subject"
        )

        if st.button(
            "Start Viva",
            key="start_viva"
        ):

            prompt = f"""
            Act as a professional college viva examiner.

            Subject: {subject}

            Ask ONLY ONE viva question.

            Do not provide the answer.

            Wait for the student's response.
            """

            with st.spinner(
                "Preparing Viva..."
            ):

                question = get_gemini_response(
                    prompt
                )

            st.session_state.viva_question = question

        if "viva_question" in st.session_state:

            st.info(
                st.session_state.viva_question
            )

            student_answer = st.text_area(
                "Your Answer",
                key="student_answer"
            )

            if st.button(
                "Evaluate Answer",
                key="evaluate_viva"
            ):

                evaluation_prompt = f"""
                You are a college viva examiner.

                Question:
                {st.session_state.viva_question}

                Student Answer:
                {student_answer}

                Evaluate:

                1. Correctness
                2. Missing Points
                3. Suggestions
                4. Score out of 10

                Give detailed feedback.
                """

                with st.spinner(
                    "Evaluating..."
                ):

                    feedback = get_gemini_response(
                        evaluation_prompt
                    )

                st.success(
                    feedback
                )


        st.divider()

        st.subheader("📝 Quiz Generator")

        quiz_topic = st.text_input(
            "Enter Topic",
            key="quiz_topic"
        )

        if st.button(
            "Generate Quiz",
            key="generate_quiz"
        ):

            prompt = f"""
            Create 5 MCQs on:

            {quiz_topic}

            Format:

            Q1.
            A)
            B)
            C)
            D)

            Correct Answer:

            Repeat for all 5 questions.
            """

            with st.spinner(
                "Generating Quiz..."
            ):

                quiz = get_gemini_response(
                    prompt
                )

            st.session_state.quiz = quiz

        if "quiz" in st.session_state:

            st.write(
                st.session_state.quiz
            )


                    # =====================================
    # TAB 4 : EXAM NIGHT MODE
    # =====================================

    with tab4:

        st.header("🚨 Exam Night Mode")

        st.warning(
            "Exam tomorrow? Don't panic. Lumina will help you revise smartly."
        )

        subject = st.text_input(
            "Enter Subject",
            key="exam_subject"
        )

        if st.button(
            "🚨 EXAM TOMORROW",
            key="exam_button"
        ):

            prompt = f"""
            You are an expert exam preparation coach.

            Subject:
            {subject}

            Generate:

            1. 1 Hour Revision Plan

            2. Most Important Topics

            3. 5 Highly Expected Exam Questions

            4. Last Minute Notes

            Make the response practical and exam-focused.
            """

            with st.spinner(
                "Generating Survival Plan..."
            ):

                result = get_gemini_response(
                    prompt
                )

            st.success(result)