import os
import sys
import shutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install

ROOT_DIR = os.path.dirname(__file__)

class my_install(install):
    def initialize_options(self):
        self.lib_dir_path = os.path.join(sys.prefix, 'lib')
        if not os.path.exists(self.lib_dir_path):
            os.mkdir(self.lib_dir_path, 0o777)

        super().initialize_options()


    def run(self):
        c_dir_path = os.path.join(ROOT_DIR, "c")
        # build libzatopos
        subprocess.run(["make"], cwd=c_dir_path)
        # copy libzatopos
        shutil.copy(
            os.path.join(c_dir_path, "build", "libzatopos.so"),
            self.lib_dir_path
        )

        super().run()


    def get_outputs(self):
        return super().get_outputs() + [os.path.join(self.lib_dir_path, "libzatopos.so")]


def get_requires():
    with open(os.path.join(ROOT_DIR, 'requirements.txt')) as f:
        requires = f.readlines()
    return requires


setup(
    name='zatopos',
    version='0.0.0',
    description='calculate position using loud footdsteps',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    author='ShinagawaKazemaru',
    author_email='kazemaru.tatsunoshin@gmail.com',
    license='MIT',

    install_requires=get_requires(),
    python_requires='>=3.9',
    packages=find_packages(where='py'),
    package_dir={'': 'py'},
    include_package_data=True,

    cmdclass={'install': my_install}
)
