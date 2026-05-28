# =========================
# IMPORTS
# =========================
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Desktop notifications (Linux / Ubuntu)
from plyer import notification


# =========================
# FOLDER PATHS
# =========================

# Folder to monitor
downloads_dir = "/home/boulalouah-hamza/Downloads"

# Destination folders
music_dir = "/home/boulalouah-hamza/Music"
video_dir = "/home/boulalouah-hamza/Videos"
pictures_dir = "/home/boulalouah-hamza/Pictures"
documents_dir = "/home/boulalouah-hamza/Documents"


# =========================
# SUPPORTED FILE TYPES
# =========================

image_extensions = [
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico"
]

video_extensions = [
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"
]

audio_extensions = [
    ".mp3", ".wav", ".flac", ".aac", ".m4a"
]

document_extensions = [
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"
]


# =========================
# NOTIFICATION SYSTEM
# =========================

def send_notification(title, message):
    """
    Send a desktop notification to the user.
    """
    notification.notify(
        title=title,
        message=message,
        timeout=3
    )


# =========================
# GENERATE UNIQUE FILE NAME
# =========================

def make_unique(dest, name):
    """
    Generate a unique file name if a file already exists.
    """
    filename, extension = splitext(name)
    counter = 1

    while exists(f"{dest}/{name}"):
        name = f"{filename}({counter}){extension}"
        counter += 1

    return name


# =========================
# MOVE FILE SAFELY
# =========================

def move_file(dest, entry, name):
    """
    Move file to destination folder safely and handle duplicates.
    """

    # If file already exists in destination, rename it
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)

        old_name = join(dest, name)
        new_name = join(dest, unique_name)

        rename(old_name, new_name)

    # Move file to destination folder
    move(entry, dest)


# =========================
# FILE SYSTEM EVENT HANDLER
# =========================

class MoverHandler(FileSystemEventHandler):

    def on_modified(self, event):
        """
        Triggered when the Downloads folder is modified.
        """

        with scandir(downloads_dir) as entries:
            for entry in entries:
                name = entry.name

                self.check_audio(entry, name)
                self.check_video(entry, name)
                self.check_image(entry, name)
                self.check_document(entry, name)

    # AUDIO FILES
    def check_audio(self, entry, name):
        for ext in audio_extensions:
            if name.lower().endswith(ext):
                move_file(music_dir, entry, name)
                logging.info(f"Audio file moved: {name}")

                send_notification(
                    "Audio file moved",
                    f"{name} was moved to Music folder"
                )
                break

    # VIDEO FILES
    def check_video(self, entry, name):
        for ext in video_extensions:
            if name.lower().endswith(ext):
                move_file(video_dir, entry, name)
                logging.info(f"Video file moved: {name}")

                send_notification(
                    "Video file moved",
                    f"{name} was moved to Videos folder"
                )
                break

    # IMAGE FILES
    def check_image(self, entry, name):
        for ext in image_extensions:
            if name.lower().endswith(ext):
                move_file(pictures_dir, entry, name)
                logging.info(f"Image file moved: {name}")

                send_notification(
                    "Image file moved",
                    f"{name} was moved to Pictures folder"
                )
                break

    # DOCUMENT FILES
    def check_document(self, entry, name):
        for ext in document_extensions:
            if name.lower().endswith(ext):
                move_file(documents_dir, entry, name)
                logging.info(f"Document file moved: {name}")

                send_notification(
                    "Document file moved",
                    f"{name} was moved to Documents folder"
                )
                break


# =========================
# MAIN PROGRAM
# =========================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    print("File organizer is running and monitoring Downloads folder...")

    observer = Observer()
    observer.schedule(MoverHandler(), downloads_dir, recursive=True)

    observer.start()

    try:
        while True:
            sleep(10)

    except KeyboardInterrupt:
        print("Stopping file organizer...")
        observer.stop()

    observer.join()