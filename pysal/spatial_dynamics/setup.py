
#!/usr/bin/env python
import sys

from os.path import join

if sys.version_info[0] >= 3:
    DEFINE_MACROS = [("SCIPY_PY3K", None)]
else:
    DEFINE_MACROS = []

def configuration(parent_package = '', top_path = None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs
    config = Configuration('spatial_dynamics', parent_package, top_path)

    config.add_data_dir('tests')
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(maintainer = "PySAL Developers",
          author = "Serge Rey",
          maintainer_email = "pysal-dev@googlegroups.com",
          description = "Computational Geometry",
          url = "http://www.pysal.org",
          license = "BSD License",
          **configuration(top_path='').todict()
          )
