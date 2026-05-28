# File Organizer (Downloads Auto Sorter)

## Overview

This project is a Python automation script that monitors the Downloads folder and automatically organizes files into appropriate directories based on their file types. It runs continuously in the background and sorts files in real time.

Supported categories:
- Music files
- Video files
- Image files
- Document files

---

## Features

- Automatic file organization from Downloads folder
- Real-time folder monitoring using watchdog
- File type detection based on extensions
- Automatic file moving to destination folders
- Desktop notifications for each move
- Cross-file conflict handling (avoids duplicate names)

---

## Requirements

- Python 3.x
- Linux operating system (recommended Ubuntu)

### Python dependencies

Install required libraries:

```bash
pip install watchdog plyer
