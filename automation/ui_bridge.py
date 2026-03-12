import pyautogui

class UIBridge:

    def open_new_chat(self):

        pyautogui.hotkey("ctrl", "n")

    def paste_prompt(self, prompt):

        pyautogui.write(prompt)

    def send(self):

        pyautogui.press("enter")


