# Content Creation Multi-Agent System

This project provides an AI-powered Content Creation Assistant that uses a multi-agent workflow to help generate high-quality blog posts tailored to specific topics, target audiences, and keywords. It streamlines the process of content creation by dividing the tasks between specialized agents for research, writing, and editing.

### Code Flow Overview

1. **Initialization**:
   - The system begins by asking the user to select a topic for their blog post from a predefined list of content topics.
   - The system then collects details about the selected topic, such as the title, keywords, and target audience.

2. **Agents**:
   - **Content Manager**: The main agent responsible for orchestrating the entire workflow. It coordinates between the research, writing, and editing agents.
   - **Research Specialist**: Conducts research and gathers relevant information to support the content creation process.
   - **Content Writer**: Generates the content for the blog post based on the gathered research and selected keywords.
   - **Content Editor**: Edits the generated content to ensure clarity, grammar, and overall quality.

3. **Workflow**:
   - **Content Selection**: The user selects a topic, and the system initializes the content creation process by collecting the necessary details (keywords, target audience, etc.).
   - **Research**: The `Research Specialist` gathers relevant information based on the selected topic.
   - **Writing**: The `Content Writer` generates the blog content using the research data, keywords, and the target audience information.
   - **Editing**: The `Content Editor` refines the draft content, ensuring it is well-written and ready for publication.
   - **Final Output**: Once the content is created and refined, the final blog post is displayed to the user.

4. **Interactive Interface**:
   - The system uses **Streamlit** to provide a user-friendly interface where users can select topics, view content generation progress, and see the final output.

---

### Getting Started

Follow these steps to set up and run the Content Creation Multi-Agent System locally:

```bash
# 1. Create and Activate Virtual Environment
uv venv .venv
source .venv/bin/activate

# 2. Install Dependencies
uv pip install -r pyproject.toml

# 3. Run the Application
uv run chainlit run main.py
