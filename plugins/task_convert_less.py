# Copyright (c) 2012 Roberto Alsina y otros.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import subprocess

from nikola.plugin_categories import LateTask
from nikola import utils

def lessify(src, dst):
  print "yay this ran"
  subprocess.check_call("lessc {src} > {dst}".format(src=src, dst=dst, shell=True))
  
          
class ConvertLess(LateTask):
  """Copy static files into the output folder."""

  name = "convert_less"

  def gen_tasks(self):
      """Copy static files into the output folder."""

      kw = {
          "themes": self.site.THEMES,
          "output_folder": self.site.config['OUTPUT_FOLDER'],
          "filters": self.site.config['FILTERS'],
      }

      flag = True
      
      for theme_name in kw['themes']:
          src = os.path.join(utils.get_theme_path(theme_name), 'assets', 'css')
          for root, dirs, files in os.walk(src):
            for src_name in files:
                if src_name.endswith('.less'):
                  flag=False
                  
                  src_file = os.path.join(root, src_name)
                  
                  dst_file_name = src_name.replace('.less', '.css')      
                  dst_file = os.path.join(root, dst_file_name)
                  
                  yield {
                      'name': str(dst_file),
                      'file_dep': [src_file],
                      'targets': [dst_file],
                      'actions': [(lessify, (src_file, dst_file))],
                      'clean': True,
                  }

      if flag:
          yield {
              'basename': self.name,
              'name': 'None',
              'uptodate': [True],
              'actions': [],
          }

