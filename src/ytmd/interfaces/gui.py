import flet as ft
import threading
from ytmd.downloader.playlist import downloadPlaylist
from pytubefix import Playlist

def main():
    def app(page):
        cancel_event = threading.Event() #cancel for all threads

        #page configuration
        page.title = "Music Download"
        page.window.width = 400
        page.window.height = 230
        page.theme_mode = 'dark'
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary = ft.Colors.LIGHT_BLUE_ACCENT
            )
        )

        #function to update progress
        def progress(completed, total):
            progress_bar.value = completed / total
            status_text.value = "Downloading Playlist"
            page.update()

            if completed == total:
                status_text.value = "Download completed!"
                page.update()

                page.dialog = ft.AlertDialog(
                    title=ft.Text("Download Completed"),
                    content=ft.Text(f"{total} songs were downloaded successfully."),
                    on_dismiss=lambda e: reset_progress()  #reset the progress bar 
                )
                page.dialog.open = True
                page.update()

        #function to handle the search button click
        def on_search(e):
            cancel_event.clear()

            if not url_field.value:
                url_field.error_text = "Insert a valid URL"
                status_text.value = "Please enter a valid URL"
                page.update()
                return

            url = url_field.value
            status_text.value = "Downloading metadata"
            page.update()

            try:
                pl = Playlist(url)
                playlist_name = pl.title if pl.title else "MyPlaylist"
            except:
                playlist_name = "MyPlaylist"

            thread = threading.Thread(
                target=downloadPlaylist,
                args=(url, progress, cancel_event, playlist_name),
                daemon=True
            )
            thread.start()

        #function to handle the cancel button click
        def on_cancel(e):
            cancel_event.set()
            status_text.value = "Download canceled"
            reset_progress()
            page.update()

        def on_close(e):
            page.window_destroy() 
        page.on_window_event = on_close

        #function to reset the progress bar and status text
        def reset_progress():
            progress_bar.value = 0.0
            status_text.value = ""
            page.update()

        # UI components
        url_field = ft.TextField(
            label="Insert URL", 
            width=350, 
            border_radius=8,
            border_color=ft.Colors.LIGHT_BLUE_ACCENT,
        )

        status_text = ft.Text(
            "", 
            size=12, 
            color=ft.Colors.GREY,
            font_family="Arial"
        )

        progress_bar = ft.ProgressBar(
            width=350, 
            height=10,
            value=0.0, 
            color=ft.Colors.LIGHT_BLUE,
            border_radius=5,
            bgcolor=ft.Colors.BLUE_GREY_50,
        )

        button_row = ft.Row(
            [
                ft.ElevatedButton(
                    "Search",
                    on_click=on_search,
                    icon="search",
                    style=ft.ButtonStyle(
                        shape=ft.StadiumBorder(),
                    )
                ),
                ft.ElevatedButton(
                    "Cancel",
                    on_click=on_cancel,
                    icon="cancel",
                    style=ft.ButtonStyle(
                        shape=ft.StadiumBorder(),
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        content = ft.Column(
            [
                ft.Row([url_field], alignment=ft.MainAxisAlignment.CENTER),
                button_row,
                ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([progress_bar], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            expand=True, 
        )
        page.add(content)
    
    ft.app(app)