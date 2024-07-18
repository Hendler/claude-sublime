import sublime
import sublime_plugin
 # Add the path to the bundled dependency
dependency_path = os.path.join(sublime.packages_path(), 'my_plugin', 'dependencies', 'anthropic')
if dependency_path not in sys.path:
    sys.path.append(dependency_path)


try:
    from anthropic import AnthropicAPI
    print("AnthropicAPI imported successfully.")
except ImportError as e:
    print(f"Failed to import AnthropicAPI: {e}")



class ClaudeChatView(sublime_plugin.WindowCommand):
    def run(self):
        self.api = None
        self.chat_view = None
        self.input_view = None
        self.setup_views()

    def setup_views(self):
        self.chat_view = self.window.new_file()
        self.chat_view.set_name("Claude Chat")
        self.chat_view.set_scratch(True)
        self.chat_view.settings().set("word_wrap", True)
        self.chat_view.settings().set("line_numbers", False)
        self.chat_view.settings().set("gutter", False)
        self.chat_view.settings().set("scroll_past_end", False)

        self.input_view = self.window.new_file()
        self.input_view.set_name("Chat Input")
        self.input_view.set_scratch(True)
        self.input_view.settings().set("word_wrap", True)

        # Set up a two-row layout
        self.window.set_layout({
            "cols": [0.0, 1.0],
            "rows": [0.0, 0.8, 1.0],
            "cells": [[0, 0, 1, 1], [0, 1, 1, 2]]
        })

        self.window.set_view_index(self.chat_view, 0, 0)
        self.window.set_view_index(self.input_view, 0, 1)

        self.window.focus_view(self.input_view)

        self.display_message("Welcome to Claude Chat! Please enter your API key to begin.")
        self.prompt_for_api_key()

    def prompt_for_api_key(self):
        self.window.show_input_panel("Enter your Anthropic API key:", "", self.on_api_key, None, None)

    def on_api_key(self, api_key):
        self.api = AnthropicAPI(api_key)
        if self.api.validate_api_key():
            self.display_message("API key validated successfully. You can now chat with Claude!")
            self.setup_input_handler()
        else:
            self.display_message("Invalid API key. Please try again.")
            self.prompt_for_api_key()

    def setup_input_handler(self):
        self.input_view.set_name("Chat Input (Ctrl+Enter to send)")
        self.input_view.settings().set("claude_chat_input", True)
        self.window.focus_view(self.input_view)

    def on_text_command(self, view, command_name, args):
        if view.settings().get("claude_chat_input") and command_name == "insert":
            if args.get("characters") == "\n" and sublime.active_window().active_view() == self.input_view:
                if self.window.active_view().sel()[0].begin() == 0:  # Check if cursor is at the start
                    return None  # Allow normal newline insertion
                self.send_message()
                return ("insert", {"characters": ""})
        return None

    def send_message(self):
        user_input = self.input_view.substr(sublime.Region(0, self.input_view.size()))
        if user_input.strip():
            self.display_message(user_input, is_user=True)
            response = self.api.send_message(user_input)
            self.display_message(response)
            self.input_view.run_command("select_all")
            self.input_view.run_command("left_delete")
        self.window.focus_view(self.input_view)

    def display_message(self, message, is_user=False):
        self.chat_view.run_command("append", {"characters": "\n\n"})
        prefix = "You: " if is_user else "Claude: "
        self.chat_view.run_command("append", {"characters": prefix + message})
        self.chat_view.run_command("move_to", {"to": "eof"})
        if not is_user:
            self.apply_syntax_highlighting(message)

    def apply_syntax_highlighting(self, message):
        # Simple code block detection (you may want to improve this)
        code_blocks = [block for block in message.split("```") if block.strip()]
        for i, block in enumerate(code_blocks):
            if i % 2 == 1:  # This is a code block
                region = self.chat_view.find(block, self.chat_view.size() - len(message))
                if region:
                    self.chat_view.add_regions(
                        "code_block_{}".format(i),
                        [region],
                        "string",
                        "",
                        sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE
                    )
