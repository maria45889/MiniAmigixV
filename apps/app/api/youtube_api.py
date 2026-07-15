"""
YouTube API integration.
"""

import logging
import yt_dlp

logger = logging.getLogger(__name__)


class YouTubeAPI:
    """Service for YouTube API interactions."""
    
    @staticmethod
    def get_video_info(url: str) -> dict:
        """
        Get information about a YouTube video.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary with video information
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'view_count': info.get('view_count'),
                    'thumbnail': info.get('thumbnail'),
                    'video_id': info.get('id'),
                    'url': url
                }
                
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            raise
    
    @staticmethod
    def search_videos(query: str, max_results: int = 10) -> list:
        """
        Search for videos on YouTube.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of video information dictionaries
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
                'max_downloads': max_results
            }
            
            search_url = f"ytsearch{max_results}:{query}"
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_url, download=False)
                
                if 'entries' not in info:
                    return []
                
                videos = []
                for entry in info['entries'][:max_results]:
                    videos.append({
                        'title': entry.get('title'),
                        'video_id': entry.get('id'),
                        'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                        'duration': entry.get('duration'),
                        'uploader': entry.get('uploader'),
                        'thumbnail': entry.get('thumbnail')
                    })
                
                return videos
                
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            raise
    
    @staticmethod
    def get_audio_stream(url: str) -> str:
        """
        Get the best audio stream URL for a video.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Audio stream URL
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'bestaudio/best'
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                for format in info['formats']:
                    if format['acodec'] != 'none' and format['vcodec'] == 'none':
                        return format['url']
                
                # Fallback to best audio with video
                return info['formats'][0]['url']
                
        except Exception as e:
            logger.error(f"Error getting audio stream: {e}")
            raise
