import requests
from PIL import Image, ImageTk
from xml.etree import ElementTree
from io import BytesIO, FileIO
import tkinter as tk
import os
from tkinter import filedialog

from dataclasses import dataclass

from pprint import pprint

@dataclass
class Post:
    sample_url: str
    file_url: str
    tags: str
    id: int

@dataclass
class TagList:
    tags: list[str]

    @classmethod
    def empty(cls):
        return cls([])
    
    def is_empty(self): return len(self.tags) == 0

@dataclass
class Config:
    listings: list[TagList]
    page: int
    path: str


class Client:

    PAGE_SIZE = 100
    POSTS = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index'

    def __init__(self):
        ...
    
    def get_posts(self, tags: list[str], limit: int = None) -> list[Post]:
        # Set limit for posts
        if limit is None: limit = self.PAGE_SIZE

        # Send request to Rule34 API
        response = requests.get(self.POSTS, params = {'tags': ' '.join(tags), 'limit': limit})
        root = ElementTree.fromstring(response.text)

        # Iterate over XML to get all post data
        results: list[Post] = []
        for post in root.findall('post'):
            kwargs = {
                'sample_url': post.get('sample_url'),
                'file_url':   post.get('file_url'),
                'tags':       post.get('tags'),
                'id':         post.get('id'),
            }
            results.append(Post(**kwargs))


        return results


class App:
    MAX_HEIGHT = 800

    def __init__(self, directory: str = None):
        self.client = Client()
        self.root = tk.Tk()
        self.current: Post = None

        self.config = Config([TagList.empty()], 0, '.')
        self.get_posts()

        self.label = tk.Label(master = self.root)
        self.label.grid(row = 2, columnspan=1000)

        config_button = tk.Button(master = self.root, text = 'Config', command = self.open_config_window)
        config_button.grid(row = 0, column = 0)
        
        refresh_button = tk.Button(master = self.root, text = 'Refresh', command = self.refresh)
        refresh_button.grid(row = 0, column = 1)

        yes_button = tk.Button(master = self.root, text = 'Yes', command = self.yes_button_handler)
        yes_button.grid(row = 1, column = 0)

        no_button = tk.Button(master = self.root, text = 'No', command = self.display_next_image)
        no_button.grid(row = 1, column = 1)

        tag_button = tk.Button(master = self.root, text = 'Dump Tags', command = self.dump_tags)
        tag_button.grid(row = 1, column = 2)

        self.display_next_image()

        self.root.mainloop()

    @staticmethod
    def ensure_directory(path: str):
        '''Checks if directory exists'''
        if os.path.isdir(path): return
        else: os.mkdir(path)

    def get_posts(self):
        '''Using app config get posts'''
        self.posts: list[Post] = []

        # If there is no listing specified, get every post
        if not self.config.listings:
            self.posts = self.client.get_posts([])
        # Else loop over all listings and add them to queue
        else:
            for tag_list in self.config.listings:
                print(f'DEBUG Tags: {tag_list}')
                self.posts += self.client.get_posts(tag_list.tags)

    def display_next_image(self):
        # Get next in queue, and chceck if it's an image
        self.current = self.posts.pop(0)
        *_, extension = self.current.file_url.split('.')

        # Loop until image is found
        while extension in ['mp4']:
            self.current = self.posts.pop(0)
            *_, extension = self.current.file_url.split('.')
        
        # Download image
        image_bytes = BytesIO(requests.get(self.current.sample_url).content)
        pil_image   = Image.open(image_bytes)
        
        # Rescale image to fit on the screen
        width, height = pil_image.size
        if height > self.MAX_HEIGHT:
            width *= self.MAX_HEIGHT / height
            height = self.MAX_HEIGHT
        pil_image = pil_image.resize((int(width), height))

        # Display image
        tk_image = ImageTk.PhotoImage(pil_image)
        self.label.config(image = tk_image)
        self.label.image = tk_image               # Prevent garbage collector

    def yes_button_handler(self):
        # Get file extension
        *_, extension = self.current.file_url.split('.')

        # Generate path
        name = f'{self.current.id}.{extension}'
        path = os.path.join(self.config.path, name)
        # Download file
        data = requests.get(self.current.file_url).content

        # Save image
        with open(path, 'wb') as file: file.write(data)

        # Display next one
        self.display_next_image()

    def set_directory(self, path: str):
        self.directory.set(path)
        self.ensure_directory(path)

    def open_config_window(self):
        cfg_window = tk.Toplevel(self.root)
        cfg_window.title('Config')

        TAG_VAR = tk.StringVar(cfg_window)
        DIR_VAR = tk.StringVar(cfg_window)

        ##
        ## tags
        ## directory

        def dialog_set_dir(var: tk.StringVar, path: str): var.set(path)

        def dialog_read_file(var: tk.StringVar, buffer: FileIO):
            data = buffer.read()
            var.set(data)

        TAG_LABEL = tk.Label(cfg_window, text = 'Tags:')
        TAG_LABEL.grid(row = 1, column = 0)

        DIR_LABEL = tk.Label(cfg_window, text = 'Directory:')
        DIR_LABEL.grid(row = 2, column = 0)

        TAG_ENTRY = tk.Entry(cfg_window, textvariable = TAG_VAR, width = 100)
        TAG_ENTRY.grid(row = 1, column = 1)

        DIR_ENTRY = tk.Entry(cfg_window, textvariable = DIR_VAR, width = 100)
        DIR_ENTRY.grid(row = 2, column = 1)

        DIR_SELECT = tk.Button(cfg_window, text = 'Select', command = lambda: dialog_set_dir(DIR_VAR, filedialog.askdirectory()))
        DIR_SELECT.grid(row = 2, column= 2)

        TAG_SELECT = tk.Button(cfg_window, text = 'Select', command = lambda: dialog_read_file(TAG_VAR, filedialog.askopenfile()))
        TAG_SELECT.grid(row = 1, column= 2)

        def get_config():
            path = DIR_VAR.get()
            tags = TAG_VAR.get().split(';')
            page = 0

            tags = [TagList(l.split(' ')) for l in tags]
            print(tags)

            return Config(tags, page, path)


        SAVE_BUTTON = tk.Button(cfg_window, text = 'Save', command = lambda:  self.save_config_popup(get_config()))
        SAVE_BUTTON.grid(row = 3, column = 0)

    def save_config_popup(self, config):
        self.config = config

    def refresh(self):
        self.get_posts()

    def dump_tags(self):

        # Generate path to file
        name = f'{self.current.id}.tag'
        path = os.path.join(self.config.path, name)

        with open(path, 'w') as file:
            file.write(self.current.tags.replace(' ', '\n'))


if __name__ == '__main__':

    APP = App('')