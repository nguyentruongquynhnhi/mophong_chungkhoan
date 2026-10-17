from data_service import load_data
from animate import make_animation

make_animation(load_data(), "out/abc.mp4", fps=21, dpi=100, step=1)