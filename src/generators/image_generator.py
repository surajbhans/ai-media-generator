import os
import requests
import base64
import io
from PIL import Image
import time
from typing import List, Optional
try:
    import torch
    from diffusers import StableDiffusionPipeline
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from config.config import Config

class ImageGenerator:
    def __init__(self, provider: str):
        self.provider = provider
        self.config = Config()

        if provider == "OpenAI DALL-E" and OPENAI_AVAILABLE:
            if self.config.OPENAI_API_KEY:
                self.client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
            else:
                raise ValueError("OpenAI API key not found in environment variables")
        elif provider == "Stable Diffusion":
            if not self.config.STABLE_DIFFUSION_API_KEY:
                raise ValueError("Stable Diffusion API key not found in environment variables")
            self.api_key = self.config.STABLE_DIFFUSION_API_KEY
            self.api_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        elif provider == "Local Diffusion":
            if TORCH_AVAILABLE:
                self.setup_local_diffusion()
            else:
                raise ImportError("PyTorch not available. Please install torch and diffusers for local generation.")

    def setup_local_diffusion(self):
        """Setup local Stable Diffusion pipeline"""
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            ).to(device)
            self.pipe.enable_attention_slicing()
        except Exception as e:
            raise Exception(f"Failed to setup local diffusion: {str(e)}")

    def generate(self, prompt: str, negative_prompt: str = "", 
                num_images: int = 1, seed: Optional[int] = None,
                size: str = "1024x1024", quality: int = 80) -> List[Image.Image]:
        """Generate images using the selected provider"""

        if self.provider == "OpenAI DALL-E":
            return self._generate_dalle(prompt, num_images, size, quality)
        elif self.provider == "Stable Diffusion":
            return self._generate_stability_ai(prompt, negative_prompt, num_images, size)
        elif self.provider == "Local Diffusion":
            return self._generate_local_diffusion(prompt, negative_prompt, num_images, seed)
        else:
            # Fallback: Generate placeholder images
            return self._generate_placeholder(prompt, num_images, size)

    def _generate_dalle(self, prompt: str, num_images: int, size: str, quality: int) -> List[Image.Image]:
        """Generate images using OpenAI DALL-E"""
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="hd" if quality > 70 else "standard",
                n=min(num_images, 1)  # DALL-E 3 supports only 1 image at a time
            )

            images = []
            for img_data in response.data:
                img_response = requests.get(img_data.url)
                img = Image.open(io.BytesIO(img_response.content))
                images.append(img)

            return images

        except Exception as e:
            raise Exception(f"DALL-E generation failed: {str(e)}")

    def _generate_stability_ai(self, prompt: str, negative_prompt: str, 
                             num_images: int, size: str) -> List[Image.Image]:
        """Generate images using Stability AI API"""
        try:
            width, height = map(int, size.split('x'))

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "text_prompts": [
                    {"text": prompt, "weight": 1.0}
                ],
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": num_images,
                "steps": 30,
            }

            if negative_prompt:
                data["text_prompts"].append({"text": negative_prompt, "weight": -1.0})

            response = requests.post(self.api_url, json=data, headers=headers)

            if response.status_code != 200:
                raise Exception(f"API request failed: {response.text}")

            images = []
            for img_data in response.json()["artifacts"]:
                img_bytes = base64.b64decode(img_data["base64"])
                img = Image.open(io.BytesIO(img_bytes))
                images.append(img)

            return images

        except Exception as e:
            raise Exception(f"Stability AI generation failed: {str(e)}")

    def _generate_local_diffusion(self, prompt: str, negative_prompt: str, 
                                 num_images: int, seed: Optional[int]) -> List[Image.Image]:
        """Generate images using local Stable Diffusion"""
        try:
            generator = None
            if seed is not None:
                generator = torch.Generator().manual_seed(seed)

            images = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_images_per_prompt=num_images,
                generator=generator,
                num_inference_steps=30,
                guidance_scale=7.5
            ).images

            return images

        except Exception as e:
            raise Exception(f"Local diffusion generation failed: {str(e)}")

    def _generate_placeholder(self, prompt: str, num_images: int, size: str) -> List[Image.Image]:
        """Generate placeholder images when APIs are not available"""
        width, height = map(int, size.split('x'))
        images = []

        for i in range(num_images):
            # Create a simple placeholder image
            img = Image.new('RGB', (width, height), color=(100, 150, 200))

            # Add some text
            try:
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(img)

                # Try to use a default font
                try:
                    font = ImageFont.load_default()
                except:
                    font = None

                # Add prompt text
                text = f"Generated Image {i+1}\n{prompt[:50]}..."
                draw.multiline_text((10, 10), text, fill=(255, 255, 255), font=font)

            except ImportError:
                pass

            images.append(img)

        return images
