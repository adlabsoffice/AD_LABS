import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"CWD: {os.getcwd()}")

try:
    import pydub
    print(f"Pydub imported: {pydub.__file__}")
except ImportError as e:
    print(f"Pydub import failed: {e}")

try:
    import moviepy
    print(f"MoviePy imported: {moviepy.__file__}")
    print(f"MoviePy Version: {moviepy.__version__}")
except ImportError as e:
    print(f"MoviePy import failed: {e}")

try:
    from moviepy import ImageClip
    print("from moviepy import ImageClip SUCCESS")
except ImportError as e:
    print(f"from moviepy import ImageClip FAILED: {e}")
