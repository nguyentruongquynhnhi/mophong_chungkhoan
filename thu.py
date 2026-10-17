from data_service import load_data
from animate import make_animation

make_animation(load_data(), "out/test.gif", max_days=70, fps=10, dpi=70, step=2)