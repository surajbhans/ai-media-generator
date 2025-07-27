import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional
import uuid
from datetime import datetime

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class FileManager:
    """Handles file operations for the AI Media Generator"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.generated_dir = self.project_root / "generated"
        self.images_dir = self.generated_dir / "images"
        self.videos_dir = self.generated_dir / "videos"
        self.temp_dir = self.generated_dir / "temp"

        # Ensure directories exist
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def save_image(self, image, filename: Optional[str] = None) -> str:
        """Save image to the images directory"""
        if filename is None:
            filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}.png"

        filepath = self.images_dir / filename

        if PIL_AVAILABLE and hasattr(image, 'save'):
            image.save(filepath, "PNG")
        else:
            # Handle as file path or binary data
            if isinstance(image, str):
                shutil.copy2(image, filepath)
            else:
                with open(filepath, 'wb') as f:
                    f.write(image)

        return str(filepath)

    def save_video(self, video_path: str, filename: Optional[str] = None) -> str:
        """Save video to the videos directory"""
        if filename is None:
            filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}.mp4"

        destination = self.videos_dir / filename
        shutil.copy2(video_path, destination)
        return str(destination)

    def save_temp_file(self, uploaded_file) -> str:
        """Save uploaded file to temporary directory"""
        filename = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
        filepath = self.temp_dir / filename

        with open(filepath, 'wb') as f:
            f.write(uploaded_file.read())

        return str(filepath)

    def cleanup_temp_files(self, max_age_hours: int = 24):
        """Clean up temporary files older than max_age_hours"""
        import time

        current_time = time.time()
        max_age_seconds = max_age_hours * 3600

        for file_path in self.temp_dir.glob("*"):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    file_path.unlink()

    def get_generated_files(self, file_type: str = "all") -> list:
        """Get list of generated files"""
        files = []

        if file_type in ["all", "images"]:
            files.extend([str(f) for f in self.images_dir.glob("*.*")])

        if file_type in ["all", "videos"]:
            files.extend([str(f) for f in self.videos_dir.glob("*.*")])

        return sorted(files, key=lambda x: os.path.getmtime(x), reverse=True)

    def delete_file(self, filepath: str) -> bool:
        """Delete a file safely"""
        try:
            Path(filepath).unlink()
            return True
        except Exception:
            return False

    def get_file_size(self, filepath: str) -> int:
        """Get file size in bytes"""
        return Path(filepath).stat().st_size

    def create_download_link(self, filepath: str) -> str:
        """Create a download link for a file"""
        return filepath
