import os
import shutil
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("soundcloud-downloader")


@mcp.tool()
def download_soundcloud(
    url: str,
    output_path: str = "",
    mode: str = "",
    limit: int = 0,
    sync: bool = False,
    archive: str = "",
    original_art: bool = False,
    overwrite_file: bool = False,
) -> str:
    """
    Download a track, playlist, or user's tracks from SoundCloud with various options.

    Args:
        url (str): SoundCloud URL to download from.
        output_path (str, optional): Directory where files should be saved.
            Defaults to $HOME/Desktop if not provided.
        mode (str, optional): Download mode; options include:
            "all"       -> Download all tracks (flag: -a)
            "uploads"   -> Download only uploads (flag: -t)
            "favorites" -> Download favorites/likes (flag: -f)
            "reposts"   -> Download reposts (flag: -r)
            "playlists" -> Download all playlists (flag: -p)
        limit (int, optional): If > 0, download only the last <limit> tracks (flag: -n).
            NOTE: This ONLY applies to a playlist.
        sync (bool, optional): If True, run in sync mode (flag: --sync) to compare with an archive file.
        archive (str, optional): Archive file to use with sync mode.
            Defaults to ~/.scdl_archive.txt if not provided.
        original_art (bool, optional): If True, download the original cover art instead of a 500x500 JPEG.
        ignore_downloaded (bool, optional): If True, skips songs that have already been downloaded.
        overwrite_file (bool, optional): If True, overwrite a song that is already downloaded.

    Returns:
        str: A status message indicating success or error details. On error, please explain the error to
        the user and how they may be able to resolve it.
    """
    # Locate the scdl executable
    scdl_bin = shutil.which("scdl")
    if scdl_bin is None:
        potential = os.path.expanduser("~/.local/bin/scdl")
        if os.path.isfile(potential):
            scdl_bin = potential
    if scdl_bin is None:
        return (
            "scdl executable is not installed. Please instruct the user to install "
            "using 'pip install scdl' or 'pipx install scdl' and ensure its directory is in your PATH."
        )

    # Build the basic command with URL
    cmd = [scdl_bin, "-l", url]

    # Determine output path
    if output_path:
        expanded_output = os.path.expandvars(os.path.expanduser(output_path))
    else:
        expanded_output = os.path.expandvars(os.path.expanduser("$HOME/Desktop"))
    cmd.extend(["--path", expanded_output])

    # Map mode to its flag if provided
    mode = mode.lower().strip()
    mode_flag = None
    if mode == "all":
        mode_flag = "-a"
    elif mode == "uploads":
        mode_flag = "-t"
    elif mode == "favorites":
        mode_flag = "-f"
    elif mode == "reposts":
        mode_flag = "-r"
    elif mode == "playlists":
        mode_flag = "-p"
    if mode_flag:
        cmd.append(mode_flag)

    # Add limit flag if limit > 0
    if limit > 0:
        cmd.extend(["-n", str(limit)])

    # If sync mode is enabled, add the --sync flag with an archive file
    if sync:
        if not archive:
            archive = os.path.expanduser("~/.scdl_archive.txt")
        else:
            archive = os.path.expandvars(os.path.expanduser(archive))
        cmd.extend(["--sync", archive])

    # Add flag for original cover art if enabled
    if original_art:
        cmd.append("--original-art")

    # Add flag to overwrite a file if already downloaded
    if overwrite_file:
        cmd.append("--overwrite")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"Download successful. Output:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Download failed: {e.stderr}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
