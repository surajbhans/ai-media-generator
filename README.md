# AI Media Generator

A comprehensive Python web application for generating images and videos using AI technology. Built with Streamlit and supporting multiple AI providers including OpenAI DALL-E, Stable Diffusion, and RunwayML.

## Features

### 🎨 Image Generation
- **OpenAI DALL-E 3**: High-quality image generation with creative interpretation
- **Stable Diffusion**: Fast, customizable image generation
- **Local Diffusion**: GPU-accelerated local image generation
- **Batch Processing**: Generate multiple images simultaneously
- **Custom Parameters**: Control size, quality, and generation settings

### 🎥 Video Generation
- **Text-to-Video**: Create videos from text descriptions
- **Image-to-Video**: Animate static images with motion effects
- **Multiple Formats**: Support for various resolutions and frame rates
- **Local Processing**: Create videos using local algorithms
- **Motion Effects**: Zoom, rotation, wave, and other animation effects

### 🖥️ User Interface
- **Modern Web Interface**: Built with Streamlit for responsive design
- **Real-time Progress**: Live generation progress tracking
- **Media Gallery**: Organized gallery with download capabilities
- **Generation History**: Complete history of all generations
- **Provider Selection**: Easy switching between AI services

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

1. **Clone or extract the project**:
   ```bash
   cd ai-media-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp config/.env.example config/.env
   ```

   Edit the `.env` file and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   RUNWAYML_API_SECRET=your_runwayml_api_key_here
   STABLE_DIFFUSION_API_KEY=your_stable_diffusion_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## Configuration

### API Keys

To use the full functionality, you'll need API keys from:

- **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/)
- **RunwayML**: Sign up at [RunwayML](https://runwayml.com/)
- **Stability AI**: Get API access from [Stability AI](https://stability.ai/)

### Local Generation

For local image generation without API keys:
- The app includes a Local Diffusion option
- Requires GPU for optimal performance
- Downloads models automatically on first use

## Usage

### Image Generation

1. **Select Provider**: Choose from OpenAI DALL-E, Stable Diffusion, or Local Diffusion
2. **Enter Prompt**: Describe the image you want to create
3. **Set Parameters**: Adjust size, quality, and other settings
4. **Generate**: Click the generate button and wait for results
5. **Download**: Save generated images to your device

### Video Generation

1. **Choose Generation Type**: Text-to-Video or Image-to-Video
2. **Input Content**: Enter text prompt or upload base image
3. **Configure Settings**: Set duration, resolution, and style
4. **Generate**: Create your video with AI
5. **Review & Download**: Preview and save your generated video

### Advanced Features

- **Negative Prompts**: Specify what to avoid in image generation
- **Batch Processing**: Generate multiple variations
- **Custom Seeds**: Reproducible generation results
- **Motion Effects**: Add dynamic effects to image-to-video conversion

## Project Structure

```
ai-media-generator/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── config/
│   ├── config.py            # Configuration settings
│   └── .env.example         # Environment variables template
├── src/
│   ├── generators/
│   │   ├── image_generator.py   # Image generation logic
│   │   └── video_generator.py   # Video generation logic
│   ├── utils/
│   │   └── file_manager.py      # File management utilities
│   └── ui/
│       └── components.py        # UI components
├── generated/               # Generated content storage
│   ├── images/             # Generated images
│   ├── videos/             # Generated videos
│   └── temp/               # Temporary files
└── static/
    └── css/
        └── style.css       # Custom styling
```

## Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **OpenAI**: API client for DALL-E
- **Diffusers**: Hugging Face diffusion models
- **Torch**: PyTorch for local AI models
- **Pillow**: Image processing
- **OpenCV**: Computer vision and video processing
- **MoviePy**: Video editing and creation

### Optional Dependencies
- **CUDA**: For GPU acceleration (recommended)
- **FFmpeg**: For advanced video processing

## Performance Optimization

### GPU Acceleration
- Install PyTorch with CUDA support for faster generation
- Local diffusion models benefit significantly from GPU usage
- Video processing is accelerated with GPU support

### Memory Management
- Large models are automatically cached
- Temporary files are cleaned up automatically
- Configure batch sizes based on available memory

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Ensure API keys are correctly set in `.env` file
   - Check API key validity and quotas
   - Verify environment variable loading

2. **Installation Problems**:
   - Use Python 3.8 or higher
   - Install dependencies in a virtual environment
   - Check for conflicting package versions

3. **Performance Issues**:
   - Enable GPU acceleration for local models
   - Reduce batch sizes for lower memory usage
   - Close other applications to free up resources

4. **Generation Failures**:
   - Check internet connection for API-based generation
   - Verify prompt content follows provider guidelines
   - Monitor API usage quotas and limits

### Error Messages

- **"API key not found"**: Add your API keys to the `.env` file
- **"GPU not available"**: Install CUDA-enabled PyTorch
- **"Model download failed"**: Check internet connection and disk space
- **"Generation timeout"**: Reduce complexity or try different parameters

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the error messages in the Streamlit interface
3. Ensure all dependencies are properly installed
4. Verify API keys and internet connectivity

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

## Acknowledgments

- OpenAI for DALL-E API
- Stability AI for Stable Diffusion
- RunwayML for video generation capabilities
- Hugging Face for diffusion models
- Streamlit for the web framework


## made by Suraj Bhan Singh
