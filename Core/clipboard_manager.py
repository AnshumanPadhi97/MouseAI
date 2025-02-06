import win32clipboard
import keyboard
import time


class ClipboardManager:
    def get_selected_text(self):
        try:
            win32clipboard.OpenClipboard()
            try:
                original_clipboard = win32clipboard.GetClipboardData()
            except:
                original_clipboard = ''
            win32clipboard.CloseClipboard()

            keyboard.send('ctrl+c')
            time.sleep(0.1)

            win32clipboard.OpenClipboard()
            try:
                selected_text = win32clipboard.GetClipboardData()
            except:
                selected_text = ''

            win32clipboard.EmptyClipboard()
            if original_clipboard:
                win32clipboard.SetClipboardText(original_clipboard)
            win32clipboard.CloseClipboard()

            return selected_text
        except:
            return ''
