"""
Usage:
     python plottimes.py < data/alarm_count_live.html
"""
import sys
import matplotlib.pyplot as plt
from extract_data_files import LOGIX500DATA as L500D

if "__main__" == __name__:
  p = L500D()
  for line in sys.stdin: p.parse_one_line(line)

  time_names = [p.files[k].strip('_') for k in sorted(p.files.keys()) if p.files[k].endswith('TIME') or p.files[k].endswith('UNRL')]

  plt.plot([v for v in getattr(p,'BITSPRBYTE')],label='bits/byte',lw=0.5)
  for time_name in time_names:
    plt.plot([1e-4*v for v in getattr(p,time_name)],label=time_name[:-4] if time_name.endswith('TIME') else time_name)
  plt.xlabel('Unsigned byte value')
  plt.ylabel('Mean processing time per iteration, ms\nOR (# of bits)/16')
  plt.legend(loc='upper left')
  plt.show()
