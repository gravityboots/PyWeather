from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['requests','datetime','customtkinter','PIL','ctypes'], 'include_files': ['assets']}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [Executable('main.py',base=base,target_name='PyWeather (v3.2.1)')]

setup(name='PyWeather™',
      version = '3.2.1',
      description = 'Modern weather app in python',
      author = 'Manu Dhulipala',
      options = {'build_exe': build_options},
      executables = executables)
