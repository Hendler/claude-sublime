import sublime
import sublime_plugin
from ..api_interaction import AnthropicAPI

class SelectExtCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the selected text or the content of the file if no text is selected
        selected_text = ""
        for region in self.view.sel():
            if not region.empty():
                # The user has selected text
                selected_text += self.view.substr(region)

        if not selected_text:
            # No text is selected, send the entire file content
            selected_text = self.view.substr(sublime.Region(0, self.view.size()))

        self.send_text(selected_text)

    def send_text(self, text):
        settings = sublime.load_settings("SublimeClaude.sublime-settings")
        api_key = settings.get("anthropic_api_key")

        if not api_key:
            # Prompt the user for their API key
            self.view.window().show_input_panel("Enter your Anthropic API key:", "", self.on_api_key, None, None)
        else:
            # Send the text to the Claude/Anthropic API
            api = AnthropicAPI(api_key)
            response = api.send_message(text)
            self.display_response(response)

    def on_api_key(self, api_key):
        api = AnthropicAPI(api_key)
        if api.validate_api_key():
            settings = sublime.load_settings("SublimeClaude.sublime-settings")
            settings.set("anthropic_api_key", api_key)
            sublime.save_settings("SublimeClaude.sublime-settings")
            sublime.message_dialog("API key validated and saved successfully.")
            # Resend the text after API key validation
            self.run(self.view.window().active_view().sel()[0])
        else:
            sublime.message_dialog("Invalid API key. Please try again.")

    def display_response(self, response):
        # For now, we'll print the response to the Sublime Text console
        print("Claude API Response:")
        print(response)
        # TODO: Implement a better way to display the response, e.g., in a new view or panel