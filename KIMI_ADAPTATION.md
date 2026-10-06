# Kimi adaptation checklist

The project is a full hakimi web PV rebuild with a pure-black background and a Hajimi kitten mascot. The reproducible chain is:

```bash
python build.py check
python build.py lyrics
python build.py dancer
python build.py pages
python build.py render --workers 4
```

Place the licensed source audio at `input/song.mp3` before rendering. The checked-in timing is 211.913 seconds at 24 fps. `out/film.mp4` is the 1280x720 deliverable and `out/film_master.mp4` is the lossless visual master.

The final local render uses the uploaded `world.execute (me) ;.mp3`, copied to `input/song.mp3`. Its 128 kbps encoding has a different SHA-256 from the 320 kbps reference listed in `input/README.md`, but its 211.906667-second timeline is aligned and `build.py check` passes with a warning.
