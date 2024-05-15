from typing import Any
from tkinter import filedialog, messagebox
import tkinter as tk
from collections import namedtuple
from pathlib import Path
from ttsvid.audio import quotes_to_audio
import scipy.io.wavfile as wavf

AUDIO_FILE_TYPES = ("Audio files", "*.mp3 *.wav *.aac *.flac *.ogg *.wma *.m4a *.aiff *.alac") 
VIDEO_FILE_TYPES = ("Video files", "*.mp4 *.avi *.mov *.wmv *.flv *.mkv *.webm *.mpeg *.mpg *.m4v *.3gp *.3g2")
TEXT_FILE_TYPES = ("Text files", "*.txt")

FormData = namedtuple("FormData", [
    "presenter_voice",
    "quotes",
    "background_music",
    "background_video",
    "pause_between_quotes"
])

class TTSVidUI:
    def __init__(self):
        self._ui_elements = self._init_ui_elements()

    def _init_ui_elements(self) -> dict[str, Any]:
        ui_elements = {}

        # Initialize the main window
        root = tk.Tk()
        root.title("TTSVid")
        ui_elements['root'] = root

        # Create a frame for the UI
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(padx=10, pady=10)
        ui_elements['frame'] = frame

        # Presenter Voice entry
        presenter_voice_label = tk.Label(frame, text="Presenter Voice")
        presenter_voice_label.grid(row=0, column=0, sticky="e")
        presenter_voice_entry = tk.Entry(frame, width=50)
        presenter_voice_entry.grid(row=0, column=1)
        browse_presenter_voice_btn = tk.Button(frame, text="Browse", command=lambda: self._browse_file(presenter_voice_entry, [AUDIO_FILE_TYPES]))
        browse_presenter_voice_btn.grid(row=0, column=2)
        ui_elements['presenter_voice_label'] = presenter_voice_label
        ui_elements['presenter_voice_entry'] = presenter_voice_entry
        ui_elements['browse_presenter_voice_btn'] = browse_presenter_voice_btn

        # Quotes entry
        def on_quotes_browse():
            filename = self._browse_file(None, [TEXT_FILE_TYPES], fill_entry=False)
            with open(filename, 'r') as f:
                text = f.read().strip()
            quotes_entry = ui_elements['quotes_entry']
            quotes_entry.delete(0.0, tk.END)
            quotes_entry.insert(0.0, text)
        quotes_label = tk.Label(frame, text="Quotes")
        quotes_label.grid(row=1, column=0, sticky="ne")
        quotes_entry = tk.Text(frame, width=50, height=10)
        quotes_entry.grid(row=1, column=1, sticky="nsew")
        browse_quotes_btn = tk.Button(frame, text="Browse", command=on_quotes_browse)
        browse_quotes_btn.grid(row=1, column=2)
        ui_elements['quotes_label'] = quotes_label
        ui_elements['quotes_entry'] = quotes_entry
        ui_elements['browse_quotes_btn'] = browse_quotes_btn

        # Allow the text widget to expand with the window
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Background Music entry
        background_music_label = tk.Label(frame, text="Background Music")
        background_music_label.grid(row=2, column=0, sticky="e")
        background_music_entry = tk.Entry(frame, width=50)
        background_music_entry.grid(row=2, column=1)
        browse_background_music_btn = tk.Button(frame, text="Browse", command=lambda: self._browse_file(background_music_entry, [AUDIO_FILE_TYPES]))
        browse_background_music_btn.grid(row=2, column=2)
        ui_elements['background_music_label'] = background_music_label
        ui_elements['background_music_entry'] = background_music_entry
        ui_elements['browse_background_music_btn'] = browse_background_music_btn

        # Background Video entry
        background_video_label = tk.Label(frame, text="Background Video")
        background_video_label.grid(row=3, column=0, sticky="e")
        background_video_entry = tk.Entry(frame, width=50)
        background_video_entry.grid(row=3, column=1)
        browse_background_video_btn = tk.Button(frame, text="Browse", command=lambda: self._browse_file(background_video_entry, [VIDEO_FILE_TYPES]))
        browse_background_video_btn.grid(row=3, column=2)
        ui_elements['background_video_label'] = background_video_label
        ui_elements['background_video_entry'] = background_video_entry
        ui_elements['browse_background_video_btn'] = browse_background_video_btn

        # Pause Between Quotes entry using Spinbox
        pause_between_quotes_label = tk.Label(frame, text="Pause Between Quotes")
        pause_between_quotes_label.grid(row=4, column=0, sticky="e")
        pause_between_quotes_spinbox = tk.Spinbox(frame, from_=0, to=5, width=10)
        pause_between_quotes_spinbox.grid(row=4, column=1, sticky="w")
        ui_elements['pause_between_quotes_label'] = pause_between_quotes_label
        ui_elements['pause_between_quotes_spinbox'] = pause_between_quotes_spinbox

        # Tooltip for Pause Between Quotes
        pause_between_quotes_tooltip = tk.Label(frame, text="Number of seconds between each quote", font=("Arial", 8))
        pause_between_quotes_tooltip.grid(row=4, column=1, sticky="e", padx=10)
        ui_elements['pause_between_quotes_tooltip'] = pause_between_quotes_tooltip

        # Preview button
        preview_button = tk.Button(frame, text="Preview", command=self._on_preview)  # TODO
        preview_button.grid(row=5, column=0, pady=10)
        preview_button_tooltip = tk.Label(frame, text="Generate the first few quotes", font=("Arial", 8))
        preview_button_tooltip.grid(row=5, column=1, sticky="w", padx=10)
        ui_elements['preview_button'] = preview_button
        ui_elements['preview_button_tooltip'] = preview_button_tooltip

        # def test(self):
        #     error_msg, form = self._get_form_data(self._ui_elements)
        #     if len(error_msg) > 0:
        #         messagebox.showerror("Error", error_msg)
        #     else:
        #         messagebox.showinfo("Data", str(form))
        # Generate button
        generate_button = tk.Button(frame, text="Generate", command=self._on_generate)
        generate_button.grid(row=5, column=1, pady=10, sticky="e")
        generate_button_tooltip = tk.Label(frame, text="Generate all quotes", font=("Arial", 8))
        generate_button_tooltip.grid(row=5, column=2, sticky="w", padx=10)
        ui_elements['generate_button'] = generate_button
        ui_elements['generate_button_tooltip'] = generate_button_tooltip

        return ui_elements

    def _browse_file(self, entry: Any, file_types: list[tuple[str, str]], fill_entry: bool = True) -> None:
        filename = filedialog.askopenfilename(filetypes=file_types)
        if fill_entry is True:
            entry.delete(0, tk.END)
            entry.insert(0, filename)
        return filename

    def _format_form_data(self, presenter_voice: str, quotes: str, background_music: str,
        background_video: str, pause_butween_quotes: str) -> tuple[str, FormData]:
            error_msg = ""
            # check all files exist
            if not Path(presenter_voice).is_file():
                error_msg += "Please specify a valid file for 'Presenter Voice'.\n"
            # if not Path(background_music).is_file():
            #     error_msg += "Please specify a valid file for 'Background Music'.\n"
            # if not Path(background_video).is_file():
            #     error_msg += "Please specify a valid file for 'Background Video'.\n"
            # check if quote is a file
            quotes_list = quotes.strip().split("\n")
            quotes_list = [quote.strip() for quote in quotes_list if len(quote) > 0]
            if len(quotes_list) == 0:
                error_msg += "Please specify at least one quote, either within the text entry or by specifying a file."
            return error_msg, FormData(
                presenter_voice, quotes_list, background_music,
                background_video, pause_butween_quotes
            )


    def _get_form_data(self, ui_elements: dict[str, Any]) -> tuple[str, FormData]:
        presenter_voice = ui_elements['presenter_voice_entry'].get()
        quotes = ui_elements['quotes_entry'].get("1.0", tk.END).strip()
        background_music = ui_elements['background_music_entry'].get()
        background_video = ui_elements['background_video_entry'].get()
        pause_between_quotes = ui_elements['pause_between_quotes_spinbox'].get()

        error_msg, form = self._format_form_data(
            presenter_voice,
            quotes,
            background_music,
            background_video,
            int(pause_between_quotes)
        )
        return error_msg, form

    def _on_preview(self):
        error_msg, form = self._get_form_data(self._ui_elements)
        preview_size = 3
        if len(error_msg) > 0:
            messagebox.showerror("Error", error_msg)
        else:
            preview_quotes = form.quotes[:preview_size] 
            presenter_audio = form.presenter_voice
            pause_seconds = form.pause_between_quotes
            self._generate_quotes(preview_quotes, presenter_audio, pause_seconds)
            messagebox.showinfo("Success", "Audio generated to 'output.wav'")

    def _on_generate(self):
        error_msg, form = self._get_form_data(self._ui_elements)
        if len(error_msg) > 0:
            messagebox.showerror("Error", error_msg)
        else:
            quotes = form.quotes
            presenter_audio = form.presenter_voice
            pause_seconds = form.pause_between_quotes
            self._generate_quotes(quotes, presenter_audio, pause_seconds)
            messagebox.showinfo("Success", "Audio generated to 'output.wav'")

    def _generate_quotes(self, quotes: list[str], presenter_audio: str, pause_seconds: int):
        audio, sr = quotes_to_audio(quotes, presenter_audio, pause_seconds)
        output_fn = "output.wav"
        wavf.write(output_fn, sr, audio)

    def start(self) -> None:
        self._ui_elements['root'].mainloop()

ui = TTSVidUI()
ui.start()