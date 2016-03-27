'''
from distutils.core import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="IN104_simulator",
        sources=["cpp/*.pyx"],
        extra_compile_args=["-std=c++11"],
        extra_link_args=["-std=c++11"]
    )
]

setup(
    ext_modules = cythonize(extensions)
)
'''


from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = "IN104_simulator",
    ext_modules = cythonize('cpp/*.pyx'),
)
