import streamlit as st
import os
import sys
from datetime import datetime
import base64
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.generators.image_generator import ImageGenerator
from src.generators.video_generator import VideoGenerator
from src.utils.file_manager import FileManager
from src.ui.components import UIComponents
from config.config import Config

# Page configuration
st.set_page_config(
    page_title="AI Media Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    css_path = Path("static/css/style.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    if 'generated_videos' not in st.session_state:
        st.session_state.generated_videos = []
    if 'generation_history' not in st.session_state:
        st.session_state.generation_history = []

def main():
    # Load custom CSS
    load_css()

    # Initialize session state
    init_session_state()

    # Initialize components
    config = Config()
    file_manager = FileManager()
    ui_components = UIComponents()

    # Main title
    st.title("🎨 AI Media Generator")
    st.markdown("Create stunning images and videos using AI technology")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Provider selection
        provider = st.selectbox(
            "Select AI Provider",
            ["OpenAI DALL-E", "Stable Diffusion", "Local Diffusion", "RunwayML"],
            help="Choose your preferred AI service"
        )

        # Generation type
        generation_type = st.radio(
            "Generation Type",
            ["Image Generation", "Video Generation", "Image to Video"],
            horizontal=True
        )

        # Quality settings
        st.subheader("Quality Settings")
        if generation_type == "Image Generation":
            image_size = st.selectbox("Image Size", ["512x512", "1024x1024", "1024x1792"])
            image_quality = st.slider("Quality", 1, 100, 80)
        elif generation_type in ["Video Generation", "Image to Video"]:
            video_duration = st.slider("Duration (seconds)", 3, 30, 5)
            video_fps = st.selectbox("FPS", [24, 30, 60], index=1)
            video_resolution = st.selectbox("Resolution", ["720p", "1080p", "4K"])

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Input section
        st.subheader("📝 Input")

        if generation_type == "Image Generation":
            prompt = st.text_area(
                "Describe the image you want to create",
                height=100,
                placeholder="A serene landscape with mountains and a lake at sunset..."
            )

            negative_prompt = st.text_area(
                "Negative prompt (what to avoid)",
                height=60,
                placeholder="blurry, low quality, distorted..."
            )

            col_img1, col_img2 = st.columns(2)
            with col_img1:
                num_images = st.slider("Number of images", 1, 4, 1)
            with col_img2:
                seed = st.number_input("Seed (optional)", value=0, help="Use 0 for random")

        elif generation_type == "Video Generation":
            prompt = st.text_area(
                "Describe the video you want to create",
                height=100,
                placeholder="A cat playing in a garden with butterflies..."
            )

            style = st.selectbox(
                "Video Style",
                ["Realistic", "Artistic", "Cinematic", "Animated", "Documentary"]
            )

        elif generation_type == "Image to Video":
            # Image upload
            uploaded_image = st.file_uploader(
                "Upload base image",
                type=['png', 'jpg', 'jpeg'],
                help="Upload an image to animate"
            )

            if uploaded_image:
                st.image(uploaded_image, caption="Base Image", use_column_width=True)

            motion_prompt = st.text_area(
                "Describe the motion/animation",
                height=80,
                placeholder="The person in the image waves their hand..."
            )

        # Generate button
        if st.button("🚀 Generate", type="primary", use_container_width=True):
            if generation_type == "Image Generation" and prompt:
                generate_images(prompt, negative_prompt, provider, num_images, seed, image_size, image_quality)
            elif generation_type == "Video Generation" and prompt:
                generate_video(prompt, provider, video_duration, video_fps, video_resolution, style)
            elif generation_type == "Image to Video" and uploaded_image and motion_prompt:
                generate_video_from_image(uploaded_image, motion_prompt, provider, video_duration, video_fps, video_resolution)

    with col2:
        # Generation history and gallery
        st.subheader("📚 Generation History")

        if st.session_state.generation_history:
            for i, item in enumerate(reversed(st.session_state.generation_history[-10:])):
                with st.expander(f"{item['type']} - {item['timestamp']}", expanded=i==0):
                    st.write(f"**Prompt:** {item['prompt']}")
                    st.write(f"**Provider:** {item['provider']}")
                    if item['type'] == 'Image':
                        st.image(item['path'], use_column_width=True)
                    else:
                        st.video(item['path'])
        else:
            st.info("No generations yet. Start creating!")

    # Gallery section
    st.subheader("🖼️ Gallery")

    tabs = st.tabs(["Images", "Videos"])

    with tabs[0]:
        if st.session_state.generated_images:
            cols = st.columns(3)
            for i, img_path in enumerate(st.session_state.generated_images):
                with cols[i % 3]:
                    if os.path.exists(img_path):
                        st.image(img_path, use_column_width=True)
                        if st.button(f"Download", key=f"download_img_{i}"):
                            download_file(img_path)
        else:
            st.info("No images generated yet.")

    with tabs[1]:
        if st.session_state.generated_videos:
            for i, video_path in enumerate(st.session_state.generated_videos):
                if os.path.exists(video_path):
                    st.video(video_path)
                    if st.button(f"Download Video {i+1}", key=f"download_vid_{i}"):
                        download_file(video_path)
        else:
            st.info("No videos generated yet.")

def generate_images(prompt, negative_prompt, provider, num_images, seed, size, quality):
    """Generate images using the selected provider"""
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.text("Initializing image generator...")
        image_generator = ImageGenerator(provider)

        progress_bar.progress(25)
        status_text.text("Generating images...")

        images = image_generator.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_images=num_images,
            seed=seed if seed != 0 else None,
            size=size,
            quality=quality
        )

        progress_bar.progress(75)
        status_text.text("Saving images...")

        file_manager = FileManager()
        saved_paths = []

        for i, image in enumerate(images):
            filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i+1}.png"
            path = file_manager.save_image(image, filename)
            saved_paths.append(path)
            st.session_state.generated_images.append(path)

        # Add to history
        st.session_state.generation_history.append({
            'type': 'Image',
            'prompt': prompt,
            'provider': provider,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'path': saved_paths[0] if saved_paths else None
        })

        progress_bar.progress(100)
        status_text.text("✅ Images generated successfully!")

        # Display generated images
        st.subheader("Generated Images")
        cols = st.columns(min(len(images), 4))
        for i, (image, path) in enumerate(zip(images, saved_paths)):
            with cols[i % len(cols)]:
                st.image(image, use_column_width=True)
                if os.path.exists(path):
                    st.download_button(
                        label="Download",
                        data=open(path, 'rb').read(),
                        file_name=f"generated_image_{i+1}.png",
                        mime="image/png"
                    )

    except Exception as e:
        st.error(f"Error generating images: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()

def generate_video(prompt, provider, duration, fps, resolution, style):
    """Generate video using the selected provider"""
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.text("Initializing video generator...")
        video_generator = VideoGenerator(provider)

        progress_bar.progress(25)
        status_text.text("Generating video (this may take several minutes)...")

        video_path = video_generator.generate(
            prompt=prompt,
            duration=duration,
            fps=fps,
            resolution=resolution,
            style=style
        )

        progress_bar.progress(90)
        status_text.text("Finalizing video...")

        st.session_state.generated_videos.append(video_path)

        # Add to history
        st.session_state.generation_history.append({
            'type': 'Video',
            'prompt': prompt,
            'provider': provider,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'path': video_path
        })

        progress_bar.progress(100)
        status_text.text("✅ Video generated successfully!")

        # Display generated video
        st.subheader("Generated Video")
        if os.path.exists(video_path):
            st.video(video_path)

            with open(video_path, 'rb') as f:
                st.download_button(
                    label="Download Video",
                    data=f.read(),
                    file_name="generated_video.mp4",
                    mime="video/mp4"
                )

    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()

def generate_video_from_image(uploaded_image, motion_prompt, provider, duration, fps, resolution):
    """Generate video from uploaded image"""
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.text("Processing uploaded image...")

        # Save uploaded image temporarily
        file_manager = FileManager()
        temp_image_path = file_manager.save_temp_file(uploaded_image)

        progress_bar.progress(25)
        status_text.text("Generating video from image...")

        video_generator = VideoGenerator(provider)
        video_path = video_generator.image_to_video(
            image_path=temp_image_path,
            motion_prompt=motion_prompt,
            duration=duration,
            fps=fps,
            resolution=resolution
        )

        progress_bar.progress(90)
        status_text.text("Finalizing video...")

        st.session_state.generated_videos.append(video_path)

        # Add to history
        st.session_state.generation_history.append({
            'type': 'Image to Video',
            'prompt': motion_prompt,
            'provider': provider,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'path': video_path
        })

        progress_bar.progress(100)
        status_text.text("✅ Video generated successfully!")

        # Display generated video
        st.subheader("Generated Video")
        if os.path.exists(video_path):
            st.video(video_path)

            with open(video_path, 'rb') as f:
                st.download_button(
                    label="Download Video",
                    data=f.read(),
                    file_name="generated_video.mp4",
                    mime="video/mp4"
                )

    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()

def download_file(file_path):
    """Handle file downloads"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
                st.download_button(
                    label="Download",
                    data=file_bytes,
                    file_name=os.path.basename(file_path),
                    mime="application/octet-stream"
                )
    except Exception as e:
        st.error(f"Error downloading file: {str(e)}")

if __name__ == "__main__":
    main()
