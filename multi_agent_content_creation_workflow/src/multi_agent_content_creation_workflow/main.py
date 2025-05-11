import asyncio
import streamlit as st
from data.content_topics import topics
from models.content import ContentContext
from agents import Runner
from multi_agents import content_manager

async def process_single_topic(title: str, keywords: list, target_audience: str):
    """Process a single content topic through the multi-agent workflow"""
    st.write("\n===== Content Creation Multi-Agent System (Single Topic) =====")

    context: ContentContext = {
        "title": title,
        "keywords": keywords,
        "target_audience": target_audience,
        "research_data": None,
        "content_draft": None,
        "tool_running": False
    }

    st.write(f"\n🔍 Processing topic: {title}")

    # Show a loading spinner while processing
    with st.spinner('Generating content... Please wait.'):
        final_result = await Runner.run(
            starting_agent=content_manager,
            input=f"We have a new blog post to create: '{title}'. Target audience: {target_audience}. Keywords: {', '.join(keywords)}.",
            context=context,
            max_turns=15
        )

    # Display the results after processing

    # Display the final content that was created
    st.subheader("=== FINAL CONTENT ===")
    if final_result.final_output:
        st.write(final_result.final_output)
    else:
        st.write("No final content was generated.")

# Streamlit UI for user inputs
def streamlit_ui():
    """Create a Streamlit interface for content creation"""
    st.title("Content Creation Multi-Agent System")

    # Add a description explaining the system's functionality
    st.markdown("""
    This system uses a multi-agent workflow to assist in creating high-quality blog posts. 
    You can select a topic, and the system will generate content tailored to your chosen audience and keywords.
    Click the button below to start the content creation process.
    """)

    # Provide options for selecting a topic from the pre-defined list
    topic = st.selectbox("Select a Topic", topics, format_func=lambda t: t['title'])

    if topic:
        st.write(f"Selected Topic: {topic['title']}")
        title = topic["title"]
        keywords = topic["keywords"]
        target_audience = topic["target_audience"]

        st.write(f"Keywords: {', '.join(keywords)}")
        st.write(f"Target Audience: {target_audience}")

        # Button to trigger content generation
        if st.button("Generate Content"):
            # Call the async function to process the topic and generate content
            asyncio.run(process_single_topic(title, keywords, target_audience))

def main():
    """Main entry point for the application"""
    streamlit_ui()

if __name__ == "__main__":
    main()
