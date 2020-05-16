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
        data = event.get_data()
        journal_path = extension.preferences['journal_path']
        full_path = os.path.expanduser(journal_path)
        header = data['header']
        content = data['content']
        with open(full_path, "a") as f:
            f.write(f'{header}\n{content}\n\n')


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        data = {
            'header': datetime.now().strftime("%d.%m.%Y %H:%M"),
            'content': event.get_argument() or ''
        }
        item = ExtensionResultItem(icon='images/icon.png',
                                   name=data['header'],
                                   description=data['content'],
                                   on_enter=ExtensionCustomAction(data))

        return RenderResultListAction([item])


if __name__ == '__main__':
    JournalExtension().run()
