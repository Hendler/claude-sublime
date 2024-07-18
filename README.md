# SublimeClaude Extension

## Overview
SublimeClaude is a Sublime Text extension that allows users to interact with the Claude/Anthropic API for AI-powered code suggestions and conversations directly within the editor, similar to VS Code Copilot.

## Features
- Chat with Claude: Engage in a conversation with Claude using a dedicated chat interface.
- Select Folder: Send the contents of all text files within a selected folder to Claude.
- Select Files: Choose multiple files to send their contents to Claude.
- Select Ext: Use the right-click context menu to add text or code to the chat with Claude.

## Installation Instructions
1. Install Package Control if you haven't already (https://packagecontrol.io/installation)
2. Open the Command Palette (Ctrl+Shift+P on Windows/Linux, Cmd+Shift+P on macOS)
3. Type "Package Control: Install Package" and press Enter
4. Search for "SublimeClaude" and press Enter to install

## Dependency Installation
This package uses Package Control's dependency system. To ensure all dependencies are installed:

1. Open Sublime Text
2. Open the Command Palette (Ctrl+Shift+P on Windows/Linux, Cmd+Shift+P on macOS)
3. Type "Package Control: Satisfy Dependencies" and press Enter
4. Wait for the installation to complete

This will install all necessary dependencies for the Claude Sublime extension to function properly.

## Usage Instructions
1. Set up your Anthropic API key in the settings (see Configuration section)
2. To start chatting with Claude:
   - Open the Command Palette and type "SublimeClaude: Open Chat"
   - Use the dedicated chat view to interact with Claude
3. To send files or folder contents:
   - Right-click in the editor or sidebar
   - Choose "SublimeClaude: Select Folder" or "SublimeClaude: Select Files"
4. To add selected text to the chat:
   - Select text in the editor
   - Right-click and choose "SublimeClaude: Add to Chat"

## Configuration
1. Go to Preferences > Package Settings > SublimeClaude > Settings
2. In the right pane (User settings), add your Anthropic API key and customize the system prompt:

```json
{
    "anthropic_api_key": "YOUR_API_KEY_HERE",
    "system_prompt": "Your custom system prompt here."
}
```

## Deploying to Package Control
To make this package available via Package Control:
1. Fork the [package_control_channel](https://github.com/wbond/package_control_channel) repository
2. Add your package details to the `repository/s.json` file:
   ```json
   {
       "name": "SublimeClaude",
       "details": "https://github.com/yourusername/SublimeClaude",
       "releases": [
           {
               "sublime_text": ">=3000",
               "tags": true
           }
       ]
   }
   ```
3. Create a pull request to the package_control_channel repository
4. Once merged, your package will be available through Package Control

For more details, visit: https://packagecontrol.io/docs/submitting_a_package

## Developer Documentation
Project structure:
- `api_interaction.py`: Handles communication with the Claude/Anthropic API
- `chat_interface.py`: Manages the chat interface within Sublime Text
- `commands/`: Contains command classes for selecting files, folders, and text
- `SublimeClaude.sublime-settings`: Default settings file

To contribute:
1. Fork the repository
2. Make your changes
3. Submit a pull request with a clear description of your modifications

For the Anthropic API documentation, visit: https://docs.anthropic.com/claude/reference/getting-started-with-the-api

## License
This project is licensed under the MIT License - see the LICENSE file for details.