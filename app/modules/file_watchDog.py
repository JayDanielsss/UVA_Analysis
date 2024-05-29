import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import sys
import os

class Watcher:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        self.event_detected = False  # Flag to indicate if an event has been detected

    def run(self):
        while True:
            self.event_detected = False
            self.observer = Observer()  # Create a new Observer instance
            event_handler = Handler(self.filename, self)
            self.observer.schedule(event_handler, self.path, recursive=True)
            self.observer.start()
            try:
                while not self.event_detected:
                    time.sleep(1)
                print("Event detected")
                self.observer.stop()
                self.observer.join()
                print("Restarting observer...")
                time.sleep(1)  # Optional: a short delay before restarting
            except KeyboardInterrupt:
                self.observer.stop()
                self.observer.join()
                print("Stopping due to keyboard interrupt")
                break
            except Exception as e:
                self.observer.stop()
                self.observer.join()
                print(f"Error: {e}")
                break

class Handler(PatternMatchingEventHandler):
    def __init__(self, filename, watcher):
        super(Handler, self).__init__(
            patterns=[filename],
            ignore_patterns=["*.tmp"],
            ignore_directories=True,
            case_sensitive=False,
        )
        self.watcher = watcher

    def on_any_event(self, event):
        print("New Spill at [{}] named [{}]".format(event.src_path, time.asctime()))
        self.watcher.event_detected = True
        return True

# if __name__ == "__main__":
#     path_to_raw_directory = os.path.join("app/data/raw")
#     path = path_to_raw_directory
#     filename = "*.root" 

#     w = Watcher(path, filename)
    
#     w.run()