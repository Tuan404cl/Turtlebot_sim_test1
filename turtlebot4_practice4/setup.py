import os
from glob import glob
from setuptools import setup, find_packages

package_name = 'turtlebot4_practice4'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name] if os.path.exists('resource/' + package_name) else []),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
        (os.path.join('share', package_name, 'scripts'), glob('scripts/*')),
        (os.path.join('share', package_name, 'docs'), glob('docs/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tuan',
    maintainer_email='student@example.com',
    description='TurtleBot 4 Practice 4: Simulation, SLAM, AMCL Localization and Nav2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'check_topics = turtlebot4_practice4.check_topics:main',
            'auto_nav_goals = turtlebot4_practice4.auto_nav_goals:main',
        ],
    },
)
