from setuptools import setup

package_name = 'spb_pkg'

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
            "btlServ = spb_pkg.botolServ:main",
            "btlDet = spb_pkg.bottle_detection:main",
            "serv2 = spb_pkg.bu_serv:main",
        ],
    },
)
