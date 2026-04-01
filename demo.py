#!/usr/bin/env python3
"""
Demo script for the Email Triage Environment
Can be used in Hugging Face Spaces or for local demonstration
"""

import streamlit as st
from email_triage_env import EmailTriageEnv, Action

def main():
    st.title("Email Triage RL Environment Demo")
    st.markdown("""
    This is a demonstration of the Email Triage reinforcement learning environment.
    The agent must classify and prioritize emails in a simulated inbox.
    """)

    # Task selection
    task = st.selectbox("Select Task Difficulty", ["easy", "medium", "hard"])

    if st.button("Start New Episode"):
        env = EmailTriageEnv(task=task)
        obs = env.reset()

        st.session_state.env = env
        st.session_state.obs = obs
        st.session_state.done = False
        st.session_state.total_reward = 0.0
        st.session_state.step_count = 0

    if 'env' in st.session_state and not st.session_state.done:
        env = st.session_state.env
        obs = st.session_state.obs

        st.subheader("Current Email")
        if obs.current_email:
            st.write(f"**Subject:** {obs.current_email.subject}")
            st.write(f"**From:** {obs.current_email.sender}")
            st.write(f"**Body:** {obs.current_email.body}")
        else:
            st.write("No more emails to process.")

        st.write(f"**Progress:** {obs.emails_processed}/{obs.total_emails}")
        st.write(f"**Task:** {obs.task_description}")

        # Action selection
        st.subheader("Choose Action")

        if task == "easy":
            categories = ["important", "not_important"]
        elif task == "medium":
            categories = ["important", "urgent", "spam"]
        else:  # hard
            categories = ["important", "urgent", "spam", "not_important"]

        col1, col2 = st.columns(2)

        with col1:
            action_type = st.radio("Action Type", ["classify", "prioritize", "next"])

        with col2:
            if action_type == "classify":
                category = st.selectbox("Category", categories)
                priority = None
            elif action_type == "prioritize" and task == "hard":
                priority = st.slider("Priority (1-20, 1=highest)", 1, 20, 10)
                category = None
            else:
                category = None
                priority = None

        if st.button("Take Action"):
            if action_type == "classify":
                action = Action(action_type="classify", category=category)
            elif action_type == "prioritize":
                action = Action(action_type="prioritize", priority=priority)
            else:
                action = Action(action_type="next")

            obs, reward, done, info = env.step(action)

            st.session_state.obs = obs
            st.session_state.done = done
            st.session_state.total_reward += reward.value
            st.session_state.step_count += 1

            st.success(f"Reward: {reward.value:.2f} - {reward.reason}")

            if done:
                final_score = env.current_task.grade(
                    env.state()["classifications"],
                    env.state()["priorities"]
                )
                st.balloons()
                st.success(f"Episode Complete! Final Score: {final_score:.2f}")

        # Display current stats
        st.subheader("Episode Stats")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Reward", f"{st.session_state.total_reward:.2f}")
        with col2:
            st.metric("Steps Taken", st.session_state.step_count)
        with col3:
            if 'env' in st.session_state:
                state = st.session_state.env.state()
                st.metric("Classifications", len(state["classifications"]))

if __name__ == "__main__":
    main()