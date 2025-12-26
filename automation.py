#!/usr/bin/env python3
"""
MoneyPrinter Automation Script

This script automates the generation and upload of YouTube Shorts videos
based on the configuration specified in automation_config.yaml.

Usage:
    python automation.py                    # Run once
    python automation.py --daemon           # Run continuously as a daemon
    python automation.py --interval 12      # Override interval (hours)
"""

import os
import sys
import time
import yaml
import logging
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
CONFIG_FILE = "automation_config.yaml"
API_URL = "http://localhost:8080/api/generate"
DEFAULT_INTERVAL_HOURS = 24


class MoneyPrinterAutomation:
    """Manages automated video generation for MoneyPrinter."""
    
    def __init__(self, config_path=CONFIG_FILE):
        """Initialize the automation with configuration."""
        self.config_path = config_path
        self.config = self.load_config()
        self.topic_index = 0
        self.setup_logging()
        
    def load_config(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            logging.error(f"Configuration file {self.config_path} not found!")
            sys.exit(1)
        except yaml.YAMLError as e:
            logging.error(f"Error parsing configuration file: {e}")
            sys.exit(1)
    
    def setup_logging(self):
        """Setup logging based on configuration."""
        log_config = self.config.get('logging', {})
        
        if not log_config.get('enabled', True):
            return
        
        log_level = getattr(logging, log_config.get('log_level', 'INFO'))
        log_file = log_config.get('log_file', 'automation.log')
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
    def get_next_topic(self):
        """Get the next video topic based on configuration."""
        topics = self.config.get('video_topics', [])
        
        if not topics:
            logging.error("No video topics configured!")
            return None
        
        selection_mode = self.config.get('topic_selection_mode', 'sequential')
        
        if selection_mode == 'random':
            import random
            topic = random.choice(topics)
        else:  # sequential
            topic = topics[self.topic_index % len(topics)]
            self.topic_index += 1
        
        return topic
    
    def generate_video(self, topic):
        """Generate a video for the given topic."""
        logging.info(f"Starting video generation for topic: {topic}")
        
        settings = self.config.get('video_settings', {})
        
        # Prepare request data
        data = {
            'videoSubject': topic,
            'aiModel': settings.get('ai_model', 'g4f'),
            'voice': settings.get('voice', 'en_us_001'),
            'paragraphNumber': settings.get('paragraph_number', 1),
            'automateYoutubeUpload': settings.get('automate_youtube_upload', False),
            'useMusic': settings.get('use_music', False),
            'zipUrl': settings.get('zip_url', ''),
            'threads': settings.get('threads', 2),
            'subtitlesPosition': settings.get('subtitles_position', 'center,bottom'),
            'customPrompt': settings.get('custom_prompt', ''),
            'color': settings.get('subtitles_color', '#FFFF00')
        }
        
        try:
            # Send request to backend
            response = requests.post(
                API_URL,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=3600  # 1 hour timeout for video generation
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('status') == 'success':
                logging.info(f"Video generated successfully: {result.get('data')}")
                logging.info(f"Message: {result.get('message')}")
                return True
            else:
                logging.error(f"Video generation failed: {result.get('message')}")
                return False
                
        except requests.exceptions.ConnectionError:
            logging.error("Could not connect to MoneyPrinter backend. Is it running?")
            logging.error("Start the backend with: cd Backend && python main.py")
            return False
        except requests.exceptions.Timeout:
            logging.error("Video generation timed out after 1 hour")
            return False
        except requests.exceptions.RequestException as e:
            logging.error(f"Error generating video: {e}")
            return False
    
    def run_once(self):
        """Run one video generation cycle."""
        if not self.config.get('enabled', False):
            logging.warning("Automation is disabled in configuration")
            return False
        
        topic = self.get_next_topic()
        if not topic:
            return False
        
        return self.generate_video(topic)
    
    def run_daemon(self, interval_hours=None):
        """Run continuously, generating videos at specified intervals."""
        if interval_hours is None:
            interval_hours = self.config.get('generation_interval_hours', DEFAULT_INTERVAL_HOURS)
        
        interval_seconds = interval_hours * 3600
        
        logging.info(f"Starting MoneyPrinter automation daemon")
        logging.info(f"Generation interval: {interval_hours} hours")
        logging.info(f"Press Ctrl+C to stop")
        
        try:
            while True:
                start_time = datetime.now()
                logging.info(f"Starting generation cycle at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                success = self.run_once()
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                if success:
                    logging.info(f"Generation cycle completed in {duration:.2f} seconds")
                else:
                    logging.warning(f"Generation cycle failed after {duration:.2f} seconds")
                
                # Calculate next run time
                next_run = start_time + timedelta(hours=interval_hours)
                wait_seconds = (next_run - datetime.now()).total_seconds()
                
                if wait_seconds > 0:
                    logging.info(f"Next generation scheduled at {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                    logging.info(f"Waiting {wait_seconds / 3600:.2f} hours...")
                    time.sleep(wait_seconds)
                else:
                    logging.warning("Generation took longer than interval, starting next cycle immediately")
                    
        except KeyboardInterrupt:
            logging.info("Automation daemon stopped by user")


def main():
    """Main entry point for the automation script."""
    parser = argparse.ArgumentParser(
        description='MoneyPrinter Automation - Automated YouTube Shorts generation'
    )
    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Run continuously as a daemon'
    )
    parser.add_argument(
        '--interval',
        type=float,
        help='Override generation interval in hours'
    )
    parser.add_argument(
        '--config',
        default=CONFIG_FILE,
        help=f'Path to configuration file (default: {CONFIG_FILE})'
    )
    
    args = parser.parse_args()
    
    # Initialize automation
    automation = MoneyPrinterAutomation(config_path=args.config)
    
    # Run based on mode
    if args.daemon:
        automation.run_daemon(interval_hours=args.interval)
    else:
        success = automation.run_once()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
