import streamlit as st
from typing import Dict, Any

class UIComponents:
    """UI components for the AI Media Generator"""

    def __init__(self):
        pass

    def render_generation_card(self, title: str, content: Dict[str, Any]):
        """Render a generation card"""
        with st.container():
            st.markdown(f"### {title}")

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**Prompt:** {content.get('prompt', 'N/A')}")
                st.write(f"**Provider:** {content.get('provider', 'N/A')}")
                st.write(f"**Timestamp:** {content.get('timestamp', 'N/A')}")

            with col2:
                if content.get('type') == 'Image':
                    st.image(content.get('path'), use_column_width=True)
                elif content.get('type') == 'Video':
                    st.video(content.get('path'))

    def render_provider_status(self, provider: str, status: str):
        """Render provider status indicator"""
        color = "green" if status == "available" else "red"
        st.markdown(f"<span style='color: {color}'>● {provider}</span>", unsafe_allow_html=True)

    def render_progress_bar(self, progress: int, message: str = ""):
        """Render a progress bar with message"""
        if message:
            st.text(message)
        return st.progress(progress)

    def render_file_grid(self, files: list, columns: int = 3):
        """Render files in a grid layout"""
        cols = st.columns(columns)

        for i, file_path in enumerate(files):
            with cols[i % columns]:
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    st.image(file_path, use_column_width=True)
                elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                    st.video(file_path)
                else:
                    st.write(f"File: {file_path}")

                if st.button(f"Download", key=f"download_{i}"):
                    return file_path

        return None

    def render_settings_panel(self):
        """Render settings panel"""
        with st.expander("⚙️ Advanced Settings"):
            st.write("Advanced configuration options")

            # Model settings
            st.subheader("Model Settings")
            enable_nsfw_filter = st.checkbox("Enable NSFW Filter", value=True)
            use_gpu = st.checkbox("Use GPU Acceleration", value=True)

            # Generation settings
            st.subheader("Generation Settings")
            max_generations = st.slider("Max Concurrent Generations", 1, 5, 2)
            auto_save = st.checkbox("Auto-save Generated Content", value=True)

            return {
                "enable_nsfw_filter": enable_nsfw_filter,
                "use_gpu": use_gpu,
                "max_generations": max_generations,
                "auto_save": auto_save
            }

    def render_api_status(self, api_statuses: Dict[str, bool]):
        """Render API connection status"""
        st.subheader("API Status")

        for api_name, status in api_statuses.items():
            if status:
                st.success(f"✅ {api_name} - Connected")
            else:
                st.error(f"❌ {api_name} - Not Available")

    def render_generation_history(self, history: list, max_items: int = 10):
        """Render generation history"""
        if not history:
            st.info("No generation history available")
            return

        st.subheader("Recent Generations")

        for i, item in enumerate(history[-max_items:]):
            with st.expander(f"{item.get('type', 'Unknown')} - {item.get('timestamp', 'Unknown')}", expanded=i==0):
                st.write(f"**Prompt:** {item.get('prompt', 'N/A')}")
                st.write(f"**Provider:** {item.get('provider', 'N/A')}")

                if item.get('path') and item.get('type') == 'Image':
                    st.image(item['path'], use_column_width=True)
                elif item.get('path') and item.get('type') == 'Video':
                    st.video(item['path'])
