import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for API keys and settings"""

    def __init__(self):
        # API Keys
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.RUNWAYML_API_SECRET = os.getenv('RUNWAYML_API_SECRET')
        self.STABLE_DIFFUSION_API_KEY = os.getenv('STABLE_DIFFUSION_API_KEY')
        self.HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

        # Paths
        self.PROJECT_ROOT = Path(__file__).parent.parent
        self.GENERATED_DIR = self.PROJECT_ROOT / "generated"
        self.IMAGES_DIR = self.GENERATED_DIR / "images"
        self.VIDEOS_DIR = self.GENERATED_DIR / "videos"
        self.TEMP_DIR = self.GENERATED_DIR / "temp"

        # Create directories if they don't exist
        self.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        self.VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        self.TEMP_DIR.mkdir(parents=True, exist_ok=True)

        # Generation settings
        self.MAX_IMAGE_SIZE = 2048
        self.MAX_VIDEO_DURATION = 60
        self.DEFAULT_FPS = 24

        # Model settings
        self.STABLE_DIFFUSION_MODEL = "runwayml/stable-diffusion-v1-5"
        self.DEVICE = "cuda" if self._check_gpu() else "cpu"

    def _check_gpu(self) -> bool:
        """Check if GPU is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def validate_api_keys(self):
        """Validate that required API keys are present"""
        missing_keys = []

        if not self.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        if not self.RUNWAYML_API_SECRET:
            missing_keys.append("RUNWAYML_API_SECRET")

        if missing_keys:
            print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
            print("Please add them to your .env file for full functionality")

        return len(missing_keys) == 0
