import sublime
import sublime_plugin
import os
from ..api_interaction import AnthropicAPI

class SelectFolderCommand(sublime_plugin.WindowCommand):
    def run(self):
        if not hasattr(self, 'api') or not self.api.validate_api_key():
            self.window.show_input_panel("Enter your Anthropic API key:", "", self.on_api_key, None, None)
        else:
            self.window.show_input_panel("Enter folder path:", "", self.on_done, None, None)

    def on_api_key(self, api_key):
        self.api = AnthropicAPI(api_key)
        if self.api.validate_api_key():
            sublime.message_dialog("API key validated successfully.")
            self.window.show_input_panel("Enter folder path:", "", self.on_done, None, None)
        else:
            sublime.message_dialog("Invalid API key. Please try again.")
            self.run()

    def on_done(self, input):
        folder_path = input.strip()
        if os.path.isdir(folder_path):
            text_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]
            self.send_files(text_files)
        else:
            sublime.message_dialog("Invalid folder path. Please try again.")

    def send_files(self, file_paths):
        for file_path in file_paths:
            with open(file_path, 'r') as file:
                file_content = file.read()
                response = self.api.send_message(file_content)
                print(f"Response for {file_path}:")
                print(response)  # Print the response to the Sublime Text console