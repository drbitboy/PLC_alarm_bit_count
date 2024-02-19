"""
...
<p class="P2"><span class="T1">Data File N10 (dec)  --  BITSPRBYTE</span></p>
...
<p class="P2"><span class="T4">N10:0         0      1      1      2      1      2      2      3      1      2 </span></p>
"""

import os
import re
import sys
import traceback

rgxLine = re.compile(r"^\s*(<[^>]+>\s*)*([^<]+)\s*(<[^>]+>)*\s*$")
rgxDataFile = re.compile(r"^Data\s+File\s+([A-Z]+[0-9]+)\s+[(][^)]+[)]\s+..\s+([A-Z0-9_]+)*$")
rgxData = re.compile(r"^([A-Z]+[0-9]+):([0-9]+)\s*([-.\s\d]+)\s*$")

class LOGIX500DATA:

  def __init__(self):
    self.files = dict()

  def err(self,obj): sys.stderr.write(f"{obj}\n")

  def parse_one_line(self,line):
    try:
      mungline = line.replace('\xa0','').strip()
      subline = rgxLine.match(mungline).groups()[1]
      try:
        filenum, filename = l = rgxDataFile.match(subline).groups()
        if filenum in self.files:
          assert filename == self.files[filenum]
          assert hasattr(self,filename)
        else:
          self.files[filenum] = filename
          setattr(self,filename,list())
          self.current_file = getattr(self,filename)
          self.current_filenum = filenum
        return
      except: pass

      try:
        filenum, offset, filedata = l = rgxData.match(subline).groups()
        assert filenum == self.current_filenum
        try:
          assert int(offset) == len(self.current_file)
          self.current_file.extend(map(int,filedata.strip().split()))
        except:
          if 'DEBUG' in os.environ:
            traceback.print_exc()
            self.err(dict(offset=offset,filenum=(filenum,self.current_filenum),L=len(self.current_file),mungline=mungline))
            sys.stderr.flush()
      except: pass

    except: pass

if "__main__" == __name__:
  parser = LOGIX500DATA()

  for line in sys.stdin:
    parser.parse_one_line(line)

  print(vars(parser))
  print(parser.files)

