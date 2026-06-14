"""
VidLang - A domain-specific language for generating viral TikTok-style videos.
Compiles .vid scripts into video generation commands with context-aware media.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

# Optional imports for media and export
import requests
from moviepy.editor import *
from PIL import Image
import numpy as np


@dataclass
class Scene:
    """Represents a single video scene."""
    duration: float = 3.0
    text: str = ""
    background_type: str = "solid"  # solid, image, video, gif
    background_url: Optional[str] = None
    background_path: Optional[str] = None
    font_size: int = 48
    text_color: str = "white"
    bg_color: str = "black"
    animation: str = "fade"  # fade, slide, zoom, none
    media_keywords: List[str] = field(default_factory=list)


class VidLangCompiler:
    """Compiles .vid script to video generation instructions."""
    
    def __init__(self, api_key_provider=None):
        self.api_key_provider = api_key_provider  # Function that returns API key
        self.scenes = []
        
    def parse(self, script: str) -> List[Scene]:
        """Parse .vid script into Scene objects."""
        lines = script.strip().split('\n')
        scenes = []
        current_scene = Scene()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Scene delimiter
            if line.startswith('---'):
                if current_scene.text or current_scene.background_url:
                    scenes.append(current_scene)
                    current_scene = Scene()
                continue
                
            # Key-value pairs
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == 'duration':
                    current_scene.duration = float(value)
                elif key == 'text':
                    current_scene.text = value
                elif key == 'bg_type':
                    current_scene.background_type = value
                elif key == 'bg_url':
                    current_scene.background_url = value
                elif key == 'bg_color':
                    current_scene.bg_color = value
                elif key == 'text_color':
                    current_scene.text_color = value
                elif key == 'font_size':
                    current_scene.font_size = int(value)
                elif key == 'animation':
                    current_scene.animation = value
                elif key == 'keywords':
                    current_scene.media_keywords = [k.strip() for k in value.split(',')]
            else:
                # Treat as text content
                current_scene.text += line + ' '
                
        if current_scene.text or current_scene.background_url:
            scenes.append(current_scene)
            
        return scenes
    
    def compile(self, script_path: Path, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """Compile a .vid file to video generation plan."""
        with open(script_path, 'r', encoding='utf-8') as f:
            script = f.read()
            
        scenes = self.parse(script)
        
        plan = {
            'script': script_path.name,
            'scenes': [],
            'total_duration': sum(s.duration for s in scenes),
            'output': str(output_path) if output_path else None
        }
        
        for i, scene in enumerate(scenes):
            scene_dict = {
                'index': i,
                'duration': scene.duration,
                'text': scene.text.strip(),
                'background_type': scene.background_type,
                'background_url': scene.background_url,
                'background_path': scene.background_path,
                'font_size': scene.font_size,
                'text_color': scene.text_color,
                'bg_color': scene.bg_color,
                'animation': scene.animation,
                'media_keywords': scene.media_keywords
            }
            plan['scenes'].append(scene_dict)
            
        return plan


class MediaFetcher:
    """Fetches media from free APIs based on context keywords."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.cache_dir = Path("media_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
    def fetch_background(self, keywords: List[str], media_type: str = "image") -> Optional[str]:
        """Fetch background media from free API.
        
        Args:
            keywords: Search terms for context
            media_type: 'image', 'gif', 'video'
            
        Returns:
            Path to downloaded file or None
        """
        if not keywords:
            return None
            
        query = '+'.join(keywords[:3])
        
        # Use Pixabay API (free, no key needed for demo, but better with key)
        if media_type == 'image':
            url = f"https://pixabay.com/api/?key={self.api_key or ''}&q={query}&image_type=photo&per_page=3"
        elif media_type == 'video':
            url = f"https://pixabay.com/api/videos/?key={self.api_key or ''}&q={query}&per_page=3"
        else:
            return None
            
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if media_type == 'image' and 'hits' in data and data['hits']:
                    # Get first image URL
                    img_url = data['hits'][0]['webformatURL']
                    return self._download_media(img_url, query)
                elif media_type == 'video' and 'hits' in data and data['hits']:
                    # Get first video URL (best quality)
                    video_url = data['hits'][0]['videos']['large']['url']
                    return self._download_media(video_url, query)
        except Exception as e:
            print(f"Media fetch error: {e}")
            
        return None
        
    def _download_media(self, url: str, name: str) -> str:
        """Download media to cache."""
        response = requests.get(url, stream=True, timeout=15)
        ext = url.split('.')[-1].split('?')[0]
        if ext not in ['jpg', 'jpeg', 'png', 'gif', 'mp4']:
            ext = 'jpg'
        filename = self.cache_dir / f"{name}_{datetime.now().timestamp()}.{ext}"
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return str(filename)


class TikTokExporter:
    """Exports video in TikTok-friendly format."""
    
    @staticmethod
    def create_video(plan: Dict[str, Any], media_fetcher: MediaFetcher, 
                     output_path: str = "output.mp4") -> bool:
        """Generate video from compilation plan."""
        clips = []
        
        for scene in plan['scenes']:
            # Get background if needed
            bg_path = scene.get('background_path')
            if not bg_path and scene.get('background_type') != 'solid':
                keywords = scene.get('media_keywords', [])
                if not keywords and scene.get('text'):
                    # Extract keywords from text
                    words = re.findall(r'\b\w+\b', scene['text'].lower())
                    keywords = [w for w in words if len(w) > 3][:3]
                
                bg_path = media_fetcher.fetch_background(
                    keywords, 
                    scene['background_type']
                )
                if bg_path:
                    scene['background_path'] = bg_path
                    
            # Create clip
            if bg_path and bg_path.endswith(('.mp4', '.gif')):
                bg_clip = VideoFileClip(bg_path).resize(height=1920).crop(x_center=1080/2, width=1080)
                bg_clip = bg_clip.subclip(0, min(bg_clip.duration, scene['duration']))
                if bg_clip.duration < scene['duration']:
                    bg_clip = bg_clip.loop(duration=scene['duration'])
            elif bg_path and bg_path.endswith(('.jpg', '.jpeg', '.png')):
                img = Image.open(bg_path)
                img_array = np.array(img.resize((1080, 1920)))
                bg_clip = ImageClip(img_array).set_duration(scene['duration'])
            else:
                # Solid color background
                bg_clip = ColorClip(size=(1080, 1920), color=(0,0,0)).set_duration(scene['duration'])
                
            # Add text
            if scene['text']:
                txt_clip = TextClip(
                    scene['text'], 
                    fontsize=scene['font_size'], 
                    color=scene['text_color'],
                    font='Arial-Bold',
                    method='caption',
                    size=(900, None)
                ).set_position(('center', 'center')).set_duration(scene['duration'])
                
                # Animation
                if scene['animation'] == 'fade':
                    txt_clip = txt_clip.fadein(0.5).fadeout(0.5)
                elif scene['animation'] == 'slide':
                    txt_clip = txt_clip.set_position(lambda t: ('center', 1920 - t*2000))
                    
                final_clip = CompositeVideoClip([bg_clip, txt_clip])
            else:
                final_clip = bg_clip
                
            clips.append(final_clip)
            
        if not clips:
            return False
            
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
        return True


# CLI entry point
def main():
    import argparse
    parser = argparse.ArgumentParser(description='VidLang Compiler')
    parser.add_argument('input', help='Input .vid file')
    parser.add_argument('-o', '--output', default='output.mp4', help='Output video file')
    parser.add_argument('--api-key', help='API key for media search (optional)')
    args = parser.parse_args()
    
    compiler = VidLangCompiler()
    plan = compiler.compile(Path(args.input))
    
    print(f"Compiled {args.input}:")
    print(f"  Scenes: {len(plan['scenes'])}")
    print(f"  Duration: {plan['total_duration']} seconds")
    
    fetcher = MediaFetcher(args.api_key)
    exporter = TikTokExporter()
    
    print("Generating video...")
    success = exporter.create_video(plan, fetcher, args.output)
    
    if success:
        print(f"Video saved to {args.output}")
    else:
        print("Failed to generate video")


if __name__ == '__main__':
    main()
