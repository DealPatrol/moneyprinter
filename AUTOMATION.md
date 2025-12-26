# MoneyPrinter Automation Guide

This guide explains how to set up and use the MoneyPrinter automation feature to automatically generate and upload YouTube Shorts videos on a schedule.

## Overview

The automation feature allows you to:
- Schedule periodic video generation (e.g., daily, hourly)
- Automatically upload videos to YouTube
- Cycle through multiple topics
- Run as a background daemon
- Configure all video generation settings

## Prerequisites

1. **MoneyPrinter Setup**: Complete the standard MoneyPrinter setup as described in [Local.md](Local.md)
2. **Environment Variables**: Configure all required environment variables in `.env`
3. **YouTube OAuth** (Optional): If you want automatic YouTube uploads, set up OAuth credentials as described in [Local.md](Local.md)
4. **Backend Running**: The MoneyPrinter backend must be running (`cd Backend && python main.py`)

## Installation

The automation script is already included in the repository. Just install the additional dependency:

```bash
pip install PyYAML==6.0.1
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Configuration

Edit the `automation_config.yaml` file to customize your automation settings:

### Basic Settings

```yaml
# Enable/disable automation
enabled: true

# How often to generate videos (in hours)
generation_interval_hours: 24
```

### Video Settings

Configure the same settings available in the web interface:

```yaml
video_settings:
  ai_model: "g4f"                    # "g4f", "gpt3.5-turbo", "gpt4", "gemmini"
  voice: "en_us_001"                 # See Frontend/index.html for all voices
  paragraph_number: 1
  threads: 2
  subtitles_position: "center,bottom"
  subtitles_color: "#FFFF00"
  use_music: false
  automate_youtube_upload: true      # Set to true to auto-upload to YouTube
  custom_prompt: ""                  # Leave empty for default
```

### Video Topics

Define topics that the automation will cycle through:

```yaml
video_topics:
  - "Interesting facts about space exploration"
  - "Amazing animal abilities"
  - "Mind-blowing scientific discoveries"
  - "Life hacks that actually work"

# How to select topics: "sequential" or "random"
topic_selection_mode: "sequential"
```

**Sequential mode**: Topics are selected in order, cycling back to the first when all are used.

**Random mode**: A random topic is selected each time.

### Logging

```yaml
logging:
  enabled: true
  log_file: "automation.log"
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR
```

## Usage

### Running Once

Generate one video and exit:

```bash
python automation.py
```

### Running as a Daemon

Run continuously, generating videos at the configured interval:

```bash
python automation.py --daemon
```

The script will:
1. Generate a video using the next topic
2. Wait for the configured interval
3. Repeat indefinitely (until stopped with Ctrl+C)

### Override Interval

Run with a custom interval (in hours):

```bash
# Generate a video every 12 hours
python automation.py --daemon --interval 12

# Generate a video every 30 minutes
python automation.py --daemon --interval 0.5
```

### Custom Configuration File

Use a different configuration file:

```bash
python automation.py --config my_config.yaml
```

## Running in the Background

### Linux/Mac

Use `nohup` to run in the background:

```bash
nohup python automation.py --daemon > automation_output.log 2>&1 &
```

Check the process:

```bash
ps aux | grep automation.py
```

Stop the automation:

```bash
# Find the process ID (PID)
ps aux | grep automation.py

# Kill the process
kill <PID>
```

### Using systemd (Linux)

A systemd service template is included: `moneyprinter-automation.service`

1. Edit the service file and update:
   - `YOUR_USERNAME` with your username
   - `/path/to/moneyprinter` with the actual path
   - `/path/to/your/python/bin` with your Python path

2. Copy the service file:

```bash
sudo cp moneyprinter-automation.service /etc/systemd/system/
```

3. Enable and start the service:

```bash
sudo systemctl enable moneyprinter-automation
sudo systemctl start moneyprinter-automation
sudo systemctl status moneyprinter-automation
```

View logs:

```bash
sudo journalctl -u moneyprinter-automation -f
```

### Windows

Use Task Scheduler:

1. Open Task Scheduler
2. Create a new task
3. Set trigger to "At startup" or specific time
4. Set action to run Python with the script:
   ```
   Program: python.exe
   Arguments: C:\path\to\moneyprinter\automation.py --daemon
   Start in: C:\path\to\moneyprinter
   ```

Or use `pythonw.exe` to run without a console window.

## Monitoring

### Log Files

Check the log file (default: `automation.log`):

```bash
# View last 50 lines
tail -n 50 automation.log

# Follow log in real-time
tail -f automation.log
```

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about automation progress
- **WARNING**: Warning messages (non-critical issues)
- **ERROR**: Error messages (critical issues)

## Troubleshooting

### "Could not connect to MoneyPrinter backend"

**Solution**: Make sure the backend is running:

```bash
cd Backend
python main.py
```

### "Configuration file not found"

**Solution**: Make sure `automation_config.yaml` exists in the same directory as `automation.py`.

### "No video topics configured"

**Solution**: Add at least one topic to the `video_topics` list in `automation_config.yaml`.

### YouTube Upload Fails

**Solution**: 
1. Ensure `client_secret.json` is in the `Backend/` directory
2. Complete the OAuth authentication flow
3. Check that your OAuth consent screen includes all required scopes

### Video Generation Times Out

**Solution**: 
- Increase the timeout in `automation.py` (default: 1 hour)
- Check system resources (CPU, memory)
- Reduce the number of threads in configuration

## Best Practices

1. **Test First**: Run `python automation.py` once to ensure everything works before running as a daemon
2. **Start Small**: Begin with longer intervals (e.g., 24 hours) and adjust as needed
3. **Monitor Logs**: Regularly check logs for errors or issues
4. **Backup Configuration**: Keep a backup of your `automation_config.yaml`
5. **Verify YouTube Uploads**: Check your YouTube channel to ensure videos are uploading correctly
6. **Topic Variety**: Use diverse topics to keep content interesting
7. **Storage Management**: Regularly clean up generated videos from the `temp/` directory

## Advanced Usage

### Multiple Configurations

Run multiple automation instances with different configurations:

```bash
# Configuration for daily tech videos
python automation.py --config tech_config.yaml --daemon &

# Configuration for daily science videos  
python automation.py --config science_config.yaml --daemon &
```

### Custom Scheduling with Cron

Instead of using daemon mode, use cron for more precise scheduling:

```bash
# Edit crontab
crontab -e

# Add entry to run at 9 AM daily
0 9 * * * cd /path/to/moneyprinter && python automation.py >> automation_cron.log 2>&1

# Run every 6 hours
0 */6 * * * cd /path/to/moneyprinter && python automation.py >> automation_cron.log 2>&1
```

## Example Workflows

### Daily Motivational Videos

```yaml
generation_interval_hours: 24
video_settings:
  ai_model: "gpt3.5-turbo"
  voice: "en_male_narration"
  automate_youtube_upload: true
video_topics:
  - "Daily motivation to start your day"
  - "Success habits of successful people"
  - "Overcoming challenges and obstacles"
topic_selection_mode: "sequential"
```

### Hourly Quick Facts

```yaml
generation_interval_hours: 1
video_settings:
  ai_model: "g4f"
  voice: "en_us_001"
  paragraph_number: 1
  automate_youtube_upload: true
video_topics:
  - "Quick science facts"
  - "Interesting history trivia"
  - "Technology tips"
topic_selection_mode: "random"
```

## Support

For issues or questions:
- Check existing issues: https://github.com/FujiwaraChoki/MoneyPrinter/issues
- Join Discord: https://dsc.gg/fuji-community
- Review logs in `automation.log` for debugging information
