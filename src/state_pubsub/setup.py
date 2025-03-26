from setuptools import find_packages, setup

package_name = 'state_pubsub'

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
    maintainer='matthewchen132',
    maintainer_email='matthewchen132@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
		'talker = state_pubsub.state_publisher:main',
                'listener = state_pubsub.state_subscriber:main',
        ],
    },
)
