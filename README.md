# SoundCloud -> mp3 MCP Server

Download songs, playlists, music from profiles, from SoundCloud to your local machine.

To install:
```bash
git clone https://github.com/arnavsurve/scdl-mcp
cd scdl-mcp
uv run mcp install server.py
```

You can use the Claude desktop client or any other LLM client that supports [MCP](https://www.anthropic.com/news/model-context-protocol). After running `uv run mcp install server.py` from the project directory, restart Claude desktop.

## Dependencies

`ffmpeg pipx`
`pipx install scdl`
