import os
from datetime import datetime

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import \
    ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.event import ItemEnterEvent, KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class JournalExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        base_dir = extension.preferences['logseq_path']
        data = event.get_data()
        append_to_logfile(os.path.expanduser(base_dir), "\n- NOW " + data['content'] + " #log")


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        data = {
            'content': event.get_argument() or ''
        }
        item = ExtensionResultItem(icon='images/icon.png',
                                   name='Logseq log',
                                   description=data['content'],
                                   on_enter=ExtensionCustomAction(data))

        return RenderResultListAction([item])


def append_to_logfile(base_dir, line):
    # Create the filename with the required pattern
    date_str = datetime.now().strftime("%Y_%m_%d")
    filename = os.path.join(base_dir, "journals", f"{date_str}.md")
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Open the file in append mode, creating it if it does not exist
    with open(filename, "a") as file:
        # Append the new line to the end of the file
        file.write(line + "\n")

if __name__ == '__main__':
    JournalExtension().run()
