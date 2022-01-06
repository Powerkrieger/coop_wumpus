from setuptools import setup

# this is for the usage as a gym environment

setup(
    name = 'coop_wumpus',
    version = '0.1',
    install_requires = ['gym', 'numpy', 'stable_baselines3'], #gym in version 0.10.0
    description = 'Coop Wumpus World environment for gym',
    author = 'die elitären 31er',
    url = 'https://github.com/Powerkrieger/coop_wumpus',
    keywords = ['wumpus world', 'wumpus', 'gym', 'coop'],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

)
