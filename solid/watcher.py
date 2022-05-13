import sys
from watchdog.observers import Observer
from watchdog.events import *
import time
import os
import subprocess

def run_script(file):
    process = subprocess.Popen(["python3", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        return process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        return ("", "process time out")
    

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def is_target(self, event):
        return self.is_target_ends(event.src_path) and not event.is_directory

    def is_target_ends(self, path):
        if not path.endswith(".py"):
            return False
        try:
            with open(path, 'rb') as f:
                content = f.read()
            if b"from solid import *" in content or b"import solid" in content:
                return True
        except:
            return True
        return False

    def on_moved(self, event):
        if self.is_target(event):
            print("file moved from {0} to {1}".format(event.src_path,event.dest_path))    
            self.on_deleted(event)
            if self.is_target_ends(event.dest_path):
                self.gen_from_py(event.dest_path)
            return
        if self.is_target_ends(event.dest_path):
            self.gen_from_py(event.dest_path)

    def get_target_file_name(self, path):
        if path.endswith('.scad.py'):
            return path[:-3]            
        return path[:-3] + ".scad"

    def on_created(self, event):
        if self.is_target(event):
            print("file created:{0}".format(event.src_path))
            self.gen_from_py(event.src_path)
            
    def gen_from_py(self, path):
        print(f"gen from py {path}")
        out, err = run_script(path)
        if err:
            print("run script {} error: {}".format(path, err))
            return
        if not out:
            print(f"run script {path} success, but no output")
            return
        with open(self.get_target_file_name(path), "wb") as f:
            f.write(out)        

    def on_deleted(self, event):
        if self.is_target(event):
            print("file deleted:{0}".format(event.src_path))
            target = self.get_target_file_name(event.src_path)
            if os.path.exists(target):
                os.remove(target)

    def on_modified(self, event):
        if self.is_target(event):
            print("file modified:{0}".format(event.src_path))
            self.gen_from_py(event.src_path)

def observe_scadpy(dir):
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, dir, True)
    observer.start()
    print("start to observe dir: {}".format(dir))
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def run():
    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print("help: please insert watch dir")
        return
    wd = os.getcwd()
    if len(sys.argv) >= 2:
        wd = sys.argv[1]
    observe_scadpy(wd)

if __name__ == "__main__":
    run()