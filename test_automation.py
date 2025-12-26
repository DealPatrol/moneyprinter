#!/usr/bin/env python3
"""
Test script for MoneyPrinter Automation

This script validates the automation functionality without making actual API calls.
"""

import os
import sys
import yaml
from automation import MoneyPrinterAutomation

def test_configuration_loading():
    """Test that configuration loads correctly."""
    print("Testing configuration loading...")
    automation = MoneyPrinterAutomation('automation_config.yaml')
    assert automation.config is not None, "Configuration should be loaded"
    assert 'enabled' in automation.config, "Configuration should have 'enabled' field"
    assert 'video_topics' in automation.config, "Configuration should have 'video_topics' field"
    print("✓ Configuration loading works")

def test_topic_selection_sequential():
    """Test sequential topic selection."""
    print("\nTesting sequential topic selection...")
    
    config = {
        'enabled': True,
        'video_topics': ['Topic 1', 'Topic 2', 'Topic 3'],
        'topic_selection_mode': 'sequential',
        'logging': {'enabled': False}
    }
    
    with open('test_sequential_config.yaml', 'w') as f:
        yaml.dump(config, f)
    
    automation = MoneyPrinterAutomation('test_sequential_config.yaml')
    
    # Test sequential selection
    topic1 = automation.get_next_topic()
    topic2 = automation.get_next_topic()
    topic3 = automation.get_next_topic()
    topic4 = automation.get_next_topic()  # Should wrap around
    
    assert topic1 == 'Topic 1', f"First topic should be 'Topic 1', got {topic1}"
    assert topic2 == 'Topic 2', f"Second topic should be 'Topic 2', got {topic2}"
    assert topic3 == 'Topic 3', f"Third topic should be 'Topic 3', got {topic3}"
    assert topic4 == 'Topic 1', f"Fourth topic should wrap to 'Topic 1', got {topic4}"
    
    os.remove('test_sequential_config.yaml')
    print("✓ Sequential topic selection works")

def test_topic_selection_random():
    """Test random topic selection."""
    print("\nTesting random topic selection...")
    
    config = {
        'enabled': True,
        'video_topics': ['Topic A', 'Topic B', 'Topic C', 'Topic D', 'Topic E'],
        'topic_selection_mode': 'random',
        'logging': {'enabled': False}
    }
    
    with open('test_random_config.yaml', 'w') as f:
        yaml.dump(config, f)
    
    automation = MoneyPrinterAutomation('test_random_config.yaml')
    
    # Get 20 topics and verify randomness
    topics = [automation.get_next_topic() for _ in range(20)]
    unique_topics = set(topics)
    
    assert len(unique_topics) >= 2, "Random selection should produce variety"
    assert all(t in config['video_topics'] for t in unique_topics), "All topics should be from config"
    
    os.remove('test_random_config.yaml')
    print("✓ Random topic selection works")

def test_empty_topics():
    """Test handling of empty topic list."""
    print("\nTesting empty topic list handling...")
    
    config = {
        'enabled': True,
        'video_topics': [],
        'logging': {'enabled': False}
    }
    
    with open('test_empty_topics.yaml', 'w') as f:
        yaml.dump(config, f)
    
    automation = MoneyPrinterAutomation('test_empty_topics.yaml')
    topic = automation.get_next_topic()
    
    assert topic is None, "Empty topic list should return None"
    
    os.remove('test_empty_topics.yaml')
    print("✓ Empty topic list handled correctly")

def test_video_settings():
    """Test video settings extraction."""
    print("\nTesting video settings...")
    
    config = {
        'enabled': True,
        'video_topics': ['Test Topic'],
        'video_settings': {
            'ai_model': 'gpt4',
            'voice': 'en_us_002',
            'paragraph_number': 3,
            'threads': 4,
            'subtitles_position': 'center,center',
            'subtitles_color': '#FF0000',
            'use_music': True,
            'automate_youtube_upload': True
        },
        'logging': {'enabled': False}
    }
    
    with open('test_settings_config.yaml', 'w') as f:
        yaml.dump(config, f)
    
    automation = MoneyPrinterAutomation('test_settings_config.yaml')
    settings = automation.config.get('video_settings', {})
    
    assert settings.get('ai_model') == 'gpt4', "AI model should be gpt4"
    assert settings.get('voice') == 'en_us_002', "Voice should be en_us_002"
    assert settings.get('paragraph_number') == 3, "Paragraph number should be 3"
    assert settings.get('threads') == 4, "Threads should be 4"
    assert settings.get('use_music') == True, "Use music should be True"
    
    os.remove('test_settings_config.yaml')
    print("✓ Video settings extracted correctly")

def main():
    """Run all tests."""
    print("=" * 60)
    print("MoneyPrinter Automation Test Suite")
    print("=" * 60)
    
    try:
        test_configuration_loading()
        test_topic_selection_sequential()
        test_topic_selection_random()
        test_empty_topics()
        test_video_settings()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
