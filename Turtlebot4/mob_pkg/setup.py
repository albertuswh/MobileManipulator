from setuptools import find_packages, setup

package_name = 'mob_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='albert',
    maintainer_email='albert@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "contr_mob = mob_pkg.mob_controller:main",
            "mob_menu = mob_pkg.mob_menu:main",
            "mqttServ = mob_pkg.mqtt_hand:main",
        ],
    },
)
