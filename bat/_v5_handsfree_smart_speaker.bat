@ECHO OFF
CALL __setpath.bat

python _v5_handsfree_smart_speaker.py debug ja,今なんじ siri
python _v5_handsfree_smart_speaker.py debug ja,今なんじ clova
python _v5_handsfree_smart_speaker.py debug ja,今なんじ google
python _v5_handsfree_smart_speaker.py debug ja,今なんじ alexa

PAUSE
