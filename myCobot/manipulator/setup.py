from setuptools import setup

package_name = 'manipulator'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='er',
    maintainer_email='er@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controller_cobot = manipulator.controller_cobot:main',
            'bottle_detection = manipulator.bottle_detection:main',
            'grab_bottle = manipulator.grab_obj:main',
        ],
    },
)
