import shutil
from pathlib import Path

from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import setup
from setuptools.extension import Extension


class CustomBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = build_dir if not self.inplace else root_dir

        self.copy_file(Path('pybbn') / '__init__.py', root_dir, target_dir)

    def copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))


setup(
    packages=[],
    ext_modules=cythonize(
        module_list=[Extension('pybbn.*', ['pybbn/**/*.py'])],
        build_dir='build',
        compiler_directives={
            'always_allow_keywords': False,
            'language_level': 3
        }
    ),
    cmdclass={
        'build_ext': CustomBuildExt
    }
)
