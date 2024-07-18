import sublime
import sublime_plugin
import os
from ..api_interaction import AnthropicAPI

class SelectFilesCommand(sublime_plugin.WindowCommand):
    def run(self):
        if not hasattr(self, 'api') or not self.api.validate_api_key():
            self.window.show_input_panel("Enter your Anthropic API key:", "", self.on_api_key, None, None)
        else:
            self.show_file_selection()

    def show_file_selection(self):
        self.window.show_quick_panel(self.get_file_list(), self.on_done, sublime.KEEP_OPEN_ON_FOCUS_LOST, -1, self.on_highlighted)

    def get_file_list(self):
        folders = self.window.folders()
        if not folders:
            return []

        file_list = []
        for folder in folders:
            for root, _, files in os.walk(folder):
                for file in files:
                    file_list.append(os.path.join(root, file))
        return file_list

    def on_api_key(self, api_key):
        self.api = AnthropicAPI(api_key)
        if self.api.validate_api_key():
            sublime.status_message("API key validated successfully")
            self.show_file_selection()
        else:
            sublime.error_message("Invalid API key. Please try again.")

    def on_done(self, index):
        if index == -1:
            return

        selected_file = self.get_file_list()[index]
        self.send_file_content(selected_file)

    def on_highlighted(self, index):
        if index != -1:
            sublime.status_message(f"File: {self.get_file_list()[index]}")

    def send_file_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            response = self.api.send_message(f"File content of {os.path.basename(file_path)}:\n\n{content}")

            output_view = self.window.create_output_panel("claude_response")
            output_view.run_command("append", {"characters": response})
            self.window.run_command("show_panel", {"panel": "output.claude_response"})

        except Exception as e:
            sublime.error_message(f"Error reading or sending file: {str(e)}")
