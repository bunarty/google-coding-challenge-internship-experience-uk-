"""A video player class."""
import random

from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self.paused = False
        self.current_video = None
        self._video_library = VideoLibrary()
        self.playlist = Playlist()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        # Fetch all the videos information
        list_of_videos = self._video_library.get_all_videos()
        # Sorting list in lexicographical order
        list_of_videos.sort(key=lambda asc: asc.video_id)
        print("Here's a list of all available videos:")
        # Loop through each line of the video.txt file
        for video in list_of_videos:
            tag_string = str(video.tags)  # Convert video tag to string allow removal of round brackets
            print(f"{video.title} ({video.video_id})" + " [" + tag_string.strip("()") + "]")  # print video information

    def play_video(self, video_id):
        """Plays the respective video.
        Args:
            video_id: The video_id to be played.
        """
        # Get videos from video library
        video = self._video_library.get_video(video_id)
        # If no such video exists
        if not video:
            print("Cannot play video: video does not exist")
            return
        if video.flag is not None:
            print(f"Cannot play video: Video is currently flagged (reason: {video.flag})")
            return
        if self.current_video is not None:
            print(f"Stopping video: {self.current_video.title}")
            print(f"Playing video: {video.title}")
            self.current_video = video
            return
        # If video exists and is input
        print(f"Playing video: {video.title}")
        self.current_video = video

    def stop_video(self):
        """Stops the current video."""
        video = self.current_video
        if video:
            print(f"Stopping video: {self.current_video.title}")
            self.current_video = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        # Get random videos from video library
        random_video = random.choice(self._video_library.get_all_videos())
        # If no such video exists
        if not random_video:
            print("Cannot play video: video does not exist")
        if self.current_video is not None:
            print(f"Stopping video: {self.current_video.title}")
            print(f"Playing video: {random_video.title}")
            self.current_video = random_video
            return
        # If video exists and is input
        print(f"Playing video: {random_video.title}")
        self.current_video = random_video

    def pause_video(self):
        """Pauses the current video."""
        if self.current_video:
            if self.paused:
                print(f"Video already paused: {self.current_video.title}")
            else:
                print(f"Pausing video: {self.current_video.title}")
                self.paused = True
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.current_video:
            if self.paused:
                print(f"Continuing video: {self.current_video.title}")
            else:
                print(f"Video already playing: {self.current_video.title}")
                self.paused = False
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        tag_string = str(self.current_video.tags)
        if self.current_video:
            if self.paused:
                print(f"{self.current_video.title} ({self.current_video.video_id})" + " [" + tag_string.strip(
                    "()") + "] - PAUSED")
            else:
                print(
                    f"{self.current_video.title} ({self.current_video.video_id})" + " [" + tag_string.strip("()") + "]")
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        new_playlist = self.playlist.get_playlist(playlist_name.lower())
        if playlist_name.lower() is new_playlist:
            print("Cannot create playlist: A playlist with the same name already exists")
        elif playlist_name.lower() is not new_playlist:
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.
        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist = self.playlist.get_playlist(playlist_name.lower())
        video = self._video_library.get_video(video_id)

        if playlist_name.lower() != playlist and video_id == video:
            self.playlist = playlist_name.lower()

            print(f"Added video to my_playlist {playlist_name}")
        if playlist_name.lower() == playlist and video_id == video:
            print(f"Cannot add video to {playlist_name}: Video already added")
        if video_id != video:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        if playlist_name.lower() != self.playlist:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        if not self.playlist:
            print("No playlists exist yet")
            return
        print("Showing all playlists:")
        for playlist in sorted(self.playlist):
            print(f"{self.playlist[playlist].name}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlist:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

        playlist = self.playlist[playlist_name.lower()]
        print(f"Showing playlist: {playlist_name}")
        if not playlist.videos:
            print("No videos here yet")
        for video in playlist.videos:
            print(video)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.lower() not in self.playlist:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return
        playlist = self.playlist[playlist_name.lower()]
        video = self._video_library.get_video(video_id)
        if not video:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return
        if video not in playlist.videos:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return
        print(f"Removed video from {playlist_name}: {video.title}")
        playlist.videos.remove(video)

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlist:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return
        print(f"Successfully removed all videos from {playlist_name}")
        self.playlist[playlist_name.lower()].videos = []

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlist:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

        print(f"Deleted playlist: {playlist_name}")
        self.playlist.pop(playlist_name.lower())

    def output_search_results(self, results, value):
        """Displays search results.
        Args:
            results: List of Videos, the search results.
            value: The value used to search.
        """
        if not results:
            print(f"No search results for {value}")
            return
        results = sorted(results, key=lambda x: x.title)
        print(f"Here are the results for {value}:")
        for i, result in enumerate(results):
            print(f"{i + 1}) {result}")
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        num = input()
        if num.isnumeric() and 0 <= int(num) <= len(results):
            self.play_video(results[int(num) - 1].video_id)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.
        Args:
            search_term: The query to be used in search.
        """
        results = []
        for video in self._video_library.get_all_videos():
            if search_term.lower() in video.title.lower() and video.flag is None:
                results.append(video)
        self.output_search_results(results, search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.
        Args:
            video_tag: The video tag to be used in search.
        """
        results = []
        for video in self._video_library.get_all_videos():
            if video_tag.lower() in video.tags and video.flag is None:
                results.append(video)
        self.output_search_results(results, video_tag)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if not video:
            print("Cannot flag video: Video does not exist")
        if video.flag is not None:
            print("Cannot flag video: Video is already flagged")
        video.set_flag(flag_reason)
        if self.current_video and self.current_video.video_id == video.video_id:
            self.stop_video()
        print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

            Args:
                video_id: The video_id to be allowed again.
            """

        video = self._video_library.get_video(video_id)
        if not self._video_library.get_video(video_id):
            print("Cannot remove flag from video: Video does not exist")
        if not video.flag:
            print("Cannot remove flag from video: Video is not flagged")

        print(f"Successfully removed flag from video: {video.title}")
        video.set_flag(None)

