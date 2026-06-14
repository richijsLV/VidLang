# VidLang - Video Generation Language

A domain-specific language for creating TikTok-style infographic videos with context-aware background media and API integration.

## 🎬 What is VidLang?

VidLang is a programming language designed specifically for generating engaging infographic videos similar to those trending on TikTok. Write simple scripts that automatically:
- Generate animated infographics and text overlays
- Find relevant background GIFs, videos, and images based on context
- Sync with music and voiceovers
- Export ready-to-upload TikTok videos

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/richijsLV/VidLang.git
cd VidLang
pip install -r requirements.txt
```

### Your First VidLang Script

Create a `.vid` file:

```vid
video "tiktok_facts" {
  title = "5 Surprising Facts About Space"
  duration = 60
  style = "infographic"
  
  scene "fact1" {
    text = "A day on Venus is longer than a year on Venus"
    duration = 8
    background = "space"
    animation = "fade"
  }
  
  scene "fact2" {
    text = "There are more stars than grains of sand on Earth"
    duration = 8
    background = "stars"
    animation = "slide"
  }
  
  music = "upbeat_short"
  voiceover = true
  export {
    format = "mp4"
    resolution = "1080x1920"
    platform = "tiktok"
  }
}
```

### Generate Video

```bash
vidlang compile my_video.vid --output my_video.mp4
```

## 🔧 Core Features

### Context-Aware Media Search

VidLang automatically searches for and integrates background media based on scene context:

```vid
scene "ocean_facts" {
  text = "Oceans cover 71% of Earth's surface"
  background {
    source = "auto"
    keywords = ["ocean", "waves", "underwater"]
    type = "video"
    fallback = "image"
  }
}
```

### API Integration

Connect your own media APIs:

```vid
api_config {
  endpoint = "YOUR_API_ENDPOINT"
  api_key = "YOUR_API_KEY"  # Provided at runtime
  search_endpoint = "/search"
  media_endpoint = "/media"
}
```

### Advanced Scene Control

```vid
scene "comparison" {
  layout = "split"
  left {
    text = "Before"
    color = "#FF0000"
  }
  right {
    text = "After"
    color = "#00FF00"
  }
  transition = "wipe"
  transition_duration = 1
}
```

## 📁 Project Structure

```
VidLang/
├── vidlang/                 # Core compiler
│   ├── __init__.py
│   ├── compiler.py          # Parses .vid files
│   ├── runtime.py           # Video generation engine
│   ├── media_fetcher.py     # Context-aware media search
│   ├── tiktok_exporter.py   # TikTok export utilities
│   └── utils.py
├── examples/                # Example .vid scripts
│   ├── tutorial.vid
│   ├── product_promo.vid
│   └── educational.vid
├── tests/                   # Unit tests
├── setup.py
├── requirements.txt
├── README.md
└── LICENSE
```

## 🎯 Use Cases

- **Educational Content**: Create fast-paced fact videos
- **Product Promotion**: Showcase features with dynamic graphics
- **Storytelling**: Generate narrative-driven short videos
- **Data Visualization**: Turn statistics into engaging animations
- **Quote Videos**: Transform text quotes into viral clips

## ⚙️ Configuration

### Environment Variables

Create `.env` file:

```env
VIDLANG_API_KEY=your_api_key
VIDLANG_API_ENDPOINT=https://your-api.com
MEDIA_CACHE_DIR=./cache
OUTPUT_DIR=./outputs
```

### Custom Media Providers

Implement your own media fetcher:

```python
from vidlang.media_fetcher import MediaFetcher

class MyMediaFetcher(MediaFetcher):
    def search(self, query, media_type='auto'):
        # Your API call here
        return media_urls
```

## 📤 Exporting to TikTok

After generating your video:

```bash
vidlang export my_video.mp4 --platform tiktok --caption "Check this out! #VidLang"
```

The exporter can also add TikTok-specific overlays, adjust aspect ratios, and optimize for the platform.

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Building from Source

```bash
python setup.py install
```

## 📝 Language Syntax Reference

### Video Block

```vid
video "name" {
  // Required
  title = string
  duration = integer (seconds)
  
  // Optional
  style = "infographic" | "story" | "slideshow"

A domain-specific language for creating TikTok-style infographic videos that automatically fetch context-aware background media and export ready-to-upload videos.

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/richijsLV/VidLang.git
cd VidLang
pip install -r requirements.txt
```

### Your First Video
Create a `.vid` file:
```vid
video "my_first_video" {
    title = "How AI Works"
    duration = 60
    fps = 30
    resolution = "1080x1920"
    music = "https://youtube.com/watch?v=example"
    voiceover = true
    voice = "female"
}

scene "intro" {
    text = "Artificial Intelligence is everywhere!"
    duration = 5
    background = "ai_technology"
    animation = "fade"
    font = "Poppins"
    color = "#FFFFFF"
    position = "center"
}

scene "facts" {
    text = "By 2025, AI will create 97M new jobs"
    duration = 4
    background = "future_work"
    animation = "slide"
}
```

Render it:
```bash
vidlang render my_first_video.vid --output output.mp4
```

## 🎬 Language Features

### Video Block
```vid
video "id" {
    title = string
    duration = integer (seconds)
    fps = integer (default 30)
    resolution = "widthxheight"
    music = string (path or YouTube URL)
    voiceover = boolean
    voice = "male" | "female" | "robot"
}
```

### Scene Block
```vid
scene "id" {
    text = string
    duration = integer
    background = string | object
    animation = "fade" | "slide" | "zoom" | "none"
    font = string
    color = hex
    position = "center" | "top" | "bottom"
}
```

### Conditional Logic
```vid
if engagement > 1000 {
    scene "viral" {
        text = "Going viral! 🔥"
    }
} else {
    scene "keep_going" {
        text = "Keep posting! 💪"
    }
}
```

### Loops
```vid
tips = ["Tip 1", "Tip 2", "Tip 3"]
foreach tip in tips {
    scene tip {
        text = tip
        duration = 3
    }
}
```

## 🔌 API Integration

Configure your API in `config.yaml`:
```yaml
api:
  key: YOUR_API_KEY
  endpoint: https://api.example.com/v1
  media_search: true
  background_fetch: true
```

## 📱 TikTok Export

```bash
vidlang export my_video.vid --platform tiktok --caption "Check this out! #viral"
```

The exporter adds TikTok-optimized metadata, watermarks, and aspect ratios.

## 🧠 Context-Aware Media

VidLang automatically searches for GIFs, videos, and images based on scene text using your API:
- Analyzes scene text for keywords
- Fetches relevant background media
- Caches results for performance

## 📁 Project Structure

```
VidLang/
├── vidlang/           # Core compiler
│   ├── __init__.py
│   ├── parser.py      # Language parser
│   ├── compiler.py    # Video generator
│   ├── media_fetcher.py  # Context-aware media search
│   └── tiktok_exporter.py # TikTok optimization
├── examples/          # Sample .vid files
├── tests/            # Unit tests
├── setup.py          # Package installer
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## 🛠️ Dependencies

- Python 3.8+
- moviepy (video editing)
- requests (API calls)
- yt-dlp (YouTube audio)
- pillow (image processing)
- opencv-python (video effects)

## 🤝 Contributing

Pull requests welcome! See CONTRIBUTING.md.

## 📄 License

MIT License

## 💬 Support

- Docs: https://docs.vidlang.dev
- Issues: GitHub Issues
- Discord: https://discord.gg/vidlang

---
**Made for creators, by creators. Start making viral TikTok videos with code today!**
