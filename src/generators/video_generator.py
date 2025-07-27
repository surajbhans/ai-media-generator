import os
import requests
import base64
import time
from typing import Optional
import uuid
from datetime import datetime
from pathlib import Path

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    from moviepy.editor import VideoFileClip, ImageSequenceClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

from config.config import Config

class VideoGenerator:
    def __init__(self, provider: str):
        self.provider = provider
        self.config = Config()

        if provider == "RunwayML":
            if not self.config.RUNWAYML_API_SECRET:
                raise ValueError("RunwayML API key not found in environment variables")

    def generate(self, prompt: str, duration: int = 5, fps: int = 24, 
                resolution: str = "1080p", style: str = "Realistic") -> str:
        """Generate video using the selected provider"""

        if self.provider == "RunwayML":
            return self._generate_runwayml(prompt, duration, fps, resolution)
        elif self.provider == "Local Video":
            return self._generate_local_video(prompt, duration, fps, resolution, style)
        else:
            return self._generate_placeholder_video(prompt, duration, fps, resolution, style)

    def image_to_video(self, image_path: str, motion_prompt: str, 
                      duration: int = 5, fps: int = 24, 
                      resolution: str = "1080p") -> str:
        """Convert image to video with motion"""

        if self.provider == "RunwayML":
            return self._image_to_video_runwayml(image_path, motion_prompt, duration)
        else:
            return self._image_to_video_local(image_path, motion_prompt, duration, fps, resolution)

    def _generate_runwayml(self, prompt: str, duration: int, fps: int, resolution: str) -> str:
        """Generate video using RunwayML (placeholder implementation)"""
        # This is a placeholder since RunwayML API integration requires specific setup
        return self._generate_placeholder_video(prompt, duration, fps, resolution, "RunwayML")

    def _generate_local_video(self, prompt: str, duration: int, fps: int, 
                             resolution: str, style: str) -> str:
        """Generate video using local methods"""
        if not CV2_AVAILABLE:
            return self._generate_placeholder_video(prompt, duration, fps, resolution, style)

        try:
            width, height = self._get_resolution_dimensions(resolution)

            # Generate frame sequence
            frames = []
            total_frames = duration * fps

            for i in range(total_frames):
                # Create animated frame based on prompt and style
                frame = self._create_animated_frame(prompt, style, i, total_frames, width, height)
                frames.append(frame)

            # Create video from frames
            timestamp = int(time.time())
            video_path = self.config.VIDEOS_DIR / f"local_video_{timestamp}.mp4"

            # Write video using OpenCV
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(video_path), fourcc, fps, (width, height))

            for frame in frames:
                out.write(frame)

            out.release()

            return str(video_path)

        except Exception as e:
            raise Exception(f"Local video generation failed: {str(e)}")

    def _image_to_video_runwayml(self, image_path: str, motion_prompt: str, duration: int) -> str:
        """Convert image to video using RunwayML (placeholder)"""
        return self._image_to_video_local(image_path, motion_prompt, duration, 24, "1080p")

    def _image_to_video_local(self, image_path: str, motion_prompt: str, 
                             duration: int, fps: int, resolution: str) -> str:
        """Convert image to video using local methods"""
        if not CV2_AVAILABLE:
            return self._generate_placeholder_video(motion_prompt, duration, fps, resolution, "Image2Video")

        try:
            # Load base image
            base_image = cv2.imread(image_path)
            if base_image is None:
                raise Exception(f"Could not load image: {image_path}")

            # Resize to target resolution
            width, height = self._get_resolution_dimensions(resolution)
            base_image = cv2.resize(base_image, (width, height))

            # Create animated frames with motion effects
            frames = []
            total_frames = duration * fps

            for i in range(total_frames):
                # Apply motion effects based on motion_prompt
                frame = self._apply_motion_effects(base_image, motion_prompt, i, total_frames)
                frames.append(frame)

            # Create video from frames
            timestamp = int(time.time())
            video_path = self.config.VIDEOS_DIR / f"i2v_local_{timestamp}.mp4"

            # Write video using OpenCV
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(video_path), fourcc, fps, (width, height))

            for frame in frames:
                out.write(frame)

            out.release()

            return str(video_path)

        except Exception as e:
            raise Exception(f"Local image-to-video failed: {str(e)}")

    def _generate_placeholder_video(self, prompt: str, duration: int, fps: int, 
                                   resolution: str, style: str) -> str:
        """Generate a placeholder video file"""
        try:
            # Create a simple text file as placeholder
            timestamp = int(time.time())
            video_path = self.config.VIDEOS_DIR / f"placeholder_video_{timestamp}.txt"

            with open(video_path, 'w') as f:
                f.write(f"Video Placeholder\n")
                f.write(f"Prompt: {prompt}\n")
                f.write(f"Duration: {duration}s\n")
                f.write(f"FPS: {fps}\n")
                f.write(f"Resolution: {resolution}\n")
                f.write(f"Style: {style}\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write("\nNote: This is a placeholder. Install cv2 and moviepy for actual video generation.")

            return str(video_path)

        except Exception as e:
            raise Exception(f"Placeholder video generation failed: {str(e)}")

    def _get_resolution_dimensions(self, resolution: str) -> tuple:
        """Get width and height for a resolution string"""
        resolution_map = {
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4K": (3840, 2160),
            "square": (1024, 1024)
        }
        return resolution_map.get(resolution, (1920, 1080))

    def _create_animated_frame(self, prompt: str, style: str, frame_num: int, 
                              total_frames: int, width: int, height: int):
        """Create an animated frame based on prompt and style"""
        if not CV2_AVAILABLE:
            return None

        # Create a simple animated frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Animate based on frame number
        progress = frame_num / total_frames

        # Create moving elements
        center_x = int(width/2 + np.sin(progress * 2 * np.pi) * width/4)
        center_y = int(height/2 + np.cos(progress * 2 * np.pi) * height/4)

        # Draw animated circle
        cv2.circle(frame, (center_x, center_y), 50, (255, 255, 255), -1)

        # Add text based on prompt
        cv2.putText(frame, prompt[:30], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255, 255, 255), 2)

        return frame

    def _apply_motion_effects(self, base_image, motion_prompt: str, 
                             frame_num: int, total_frames: int):
        """Apply motion effects to base image"""
        if not CV2_AVAILABLE:
            return base_image

        frame = base_image.copy()
        progress = frame_num / total_frames

        # Apply different motion effects based on prompt
        if "zoom" in motion_prompt.lower():
            # Zoom effect
            scale = 1.0 + 0.2 * progress
            center = (base_image.shape[1]//2, base_image.shape[0]//2)
            matrix = cv2.getRotationMatrix2D(center, 0, scale)
            frame = cv2.warpAffine(frame, matrix, (base_image.shape[1], base_image.shape[0]))

        elif "wave" in motion_prompt.lower():
            # Wave effect
            rows, cols = frame.shape[:2]
            wave_amp = 20 * np.sin(progress * 2 * np.pi)

            for i in range(0, rows, 4):  # Skip some rows for performance
                for j in range(0, cols, 4):  # Skip some columns for performance
                    offset_x = int(wave_amp * np.sin(2 * np.pi * i / 50))
                    offset_y = int(wave_amp * np.sin(2 * np.pi * j / 50))

                    if 0 <= i + offset_y < rows and 0 <= j + offset_x < cols:
                        frame[i, j] = base_image[i + offset_y, j + offset_x]

        elif "rotate" in motion_prompt.lower():
            # Rotation effect
            angle = 360 * progress
            center = (base_image.shape[1]//2, base_image.shape[0]//2)
            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            frame = cv2.warpAffine(frame, matrix, (base_image.shape[1], base_image.shape[0]))

        return frame
