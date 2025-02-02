import win32clipboard
import keyboard
import time


def get_selected_text():
    try:
        # Save current clipboard content
        win32clipboard.OpenClipboard()
        try:
            original_clipboard = win32clipboard.GetClipboardData()
        except:
            original_clipboard = ''
        win32clipboard.CloseClipboard()

        # Simulate Ctrl+C to copy selected text
        keyboard.send('ctrl+c')
        # Small delay to ensure the clipboard is updated
        time.sleep(0.1)

        # Get the selected text from clipboard
        win32clipboard.OpenClipboard()
        try:
            selected_text = win32clipboard.GetClipboardData()
        except:
            selected_text = ''

        # Restore original clipboard content
        win32clipboard.EmptyClipboard()
        if original_clipboard:
            win32clipboard.SetClipboardText(original_clipboard)
        win32clipboard.CloseClipboard()

        return selected_text
    except:
        return ''


def on_hotkey():
    selected_text = get_selected_text()
    if selected_text.strip():
        print(f"Selected text: {selected_text}")


def main():
    print("Text Selection Monitor running...")
    print("Select text and press Ctrl+Space to display it")
    print("Press Ctrl+Q to quit")

    # Register the hotkey
    keyboard.add_hotkey('ctrl+space', on_hotkey)

    # Wait for Ctrl+Q to exit
    keyboard.wait('ctrl+q')


if __name__ == "__main__":
    main()
