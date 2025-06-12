from setuptools import find_packages, setup

package_name = 'rsia_tests_node'

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
    maintainer='manu',
    maintainer_email='yguel@unistra.fr',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rsia_tests_node = rsia_tests_node.rsia_tests_node:main',
            'rsia_with_timeouts_tests_node = rsia_tests_node.rsia_with_timeouts_tests_node:main',
            'srv_a_node = rsia_tests_node.srv_a_test_node:main',
            'srv_b_node = rsia_tests_node.srv_b_test_node:main'
        ],
    },
)
