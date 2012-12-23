def configuation(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('pysal', parent_package, top_path)
    config.add_subpackage('cg)'
    config.add_subpackage('esda')
    config.add_subpackage('spatial_dynamics')
    config.add_subpackage('spreg')
    config.add_subpackage('inequality')
    config.add_subpackage('core')
    config.add_subpackage('contrib')
    config.add_subpackage('network')
    config.add_subpackage('region')
    config.add_subpackage('weights')
    config.make_config_py()
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
