import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../sources')
import create_synthetic_signals
import det_rep
import visu
import lkeypoints

synthetic_signal, time_vector = create_synthetic_signals.generate_signal_manually()
keypoints = lkeypoints.load_synthetic_signals(synthetic_signal , time_vector)