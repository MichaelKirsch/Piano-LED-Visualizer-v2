"""Mock API routes for local web UI development."""

import math
import os
import time

from flask import Response, jsonify, render_template, request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SONGS_DIR = os.path.join(ROOT, "Songs")


def _list_mid_files():
    if not os.path.isdir(SONGS_DIR):
        return []
    return sorted(
        f for f in os.listdir(SONGS_DIR)
        if f.endswith(".mid") and "_#" not in f
    )


def _sheet_music_path(mid_filename):
    base = mid_filename.replace(".mid", "")
    for ext in (".musicxml", ".xml", ".mxl", ".abc"):
        path = os.path.join(SONGS_DIR, base + ext)
        if os.path.exists(path):
            return path
    return None


def register_dev_api(app):
    @app.route("/api/get_songs", methods=["GET"])
    def api_get_songs():
        page = int(request.args.get("page", 1)) - 1
        length = int(request.args.get("length", 10))
        sortby = request.args.get("sortby", "dateAsc")
        search = (request.args.get("search") or "").lower()

        songs = _list_mid_files()
        if sortby == "nameAsc":
            songs.sort()
        elif sortby == "nameDesc":
            songs.sort(reverse=True)
        else:
            songs.sort(key=lambda s: os.path.getmtime(os.path.join(SONGS_DIR, s)), reverse=(sortby == "dateAsc"))

        if search:
            songs = [s for s in songs if search in s.lower()]

        total_songs = len(songs)
        max_page = max(1, int(math.ceil(total_songs / length))) if length else 1
        start = page * length
        page_songs = songs[start : start + length]

        songs_list_dict = {
            song: os.path.getmtime(os.path.join(SONGS_DIR, song))
            for song in page_songs
        }

        return render_template(
            "songs_list.html",
            len=len(songs_list_dict),
            songs_list_dict=songs_list_dict,
            page=page,
            max_page=max_page,
            total_songs=total_songs,
        )

    @app.route("/api/get_song_list_setting", methods=["GET"])
    def api_get_song_list_setting():
        return jsonify(songs_per_page=10, sort_by="dateAsc")

    @app.route("/api/get_recording_status", methods=["GET"])
    def api_get_recording_status():
        return jsonify(
            input_port="",
            play_port="",
            isrecording=False,
            isplaying=False,
        )

    @app.route("/api/get_learning_status", methods=["GET"])
    def api_get_learning_status():
        return jsonify(
            loading=False,
            is_loop_active=False,
            practice=0,
            hands=0,
            mute_hand=0,
            show_wrong_notes=True,
            show_future_notes=True,
            number_of_mistakes=0,
            start_point=0,
            end_point=100,
            set_tempo=100,
            hand_colorR=[255, 0, 0],
            hand_colorL=[0, 0, 255],
            prev_hand_colorR=[255, 0, 0],
            prev_hand_colorL=[0, 0, 255],
            is_led_activeL=True,
            is_led_activeR=True,
            hand_colorList=[[255, 0, 0], [0, 0, 255], [0, 255, 0], [255, 255, 0]],
        )

    @app.route("/api/get_settings", methods=["GET"])
    def api_get_settings():
        return jsonify(
            practice_tool_url="https://piano-visualizer.pages.dev",
            input_port="",
            play_port="",
            practice=0,
        )

    @app.route("/api/get_profiles", methods=["GET"])
    def api_get_profiles():
        return jsonify(success=True, profiles=[])

    @app.route("/api/get_current_profile", methods=["GET"])
    def api_get_current_profile():
        return jsonify(success=True, profile_id=None)

    @app.route("/api/set_current_profile", methods=["POST"])
    def api_set_current_profile():
        return jsonify(success=True)

    @app.route("/api/get_highscores", methods=["GET"])
    def api_get_highscores():
        return jsonify(success=True, highscores=[])

    @app.route("/api/change_setting", methods=["GET"])
    def api_change_setting():
        setting_name = request.args.get("setting_name", "")
        value = request.args.get("value", "")

        if setting_name == "download_sheet_music":
            path = _sheet_music_path(value)
            if not path:
                return Response("Sheet music not found", status=404, mimetype="text/plain")
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                return Response(handle.read(), mimetype="text/plain")

        if setting_name in {
            "learning_load_song",
            "start_learning_song",
            "stop_learning_song",
            "start_midi_play",
            "stop_midi_play",
            "change_practice",
            "change_tempo",
            "change_learning_loop",
            "sort_by",
            "clean_ledstrip",
        }:
            extra = {}
            if setting_name == "learning_load_song":
                extra["reload_learning_settings"] = True
            if setting_name in {"start_midi_play", "stop_midi_play"}:
                extra["reload_songs"] = True
            return jsonify(success=True, **extra)

        return jsonify(success=True)

    @app.route("/api/set_practice_active", methods=["POST"])
    def api_set_practice_active():
        return jsonify(success=True)

    @app.route("/api/clear_websocket_midi_queue", methods=["POST"])
    def api_clear_websocket_midi_queue():
        return jsonify(success=True)

    print(f"Dev API: {len(_list_mid_files())} song(s) in Songs/")
