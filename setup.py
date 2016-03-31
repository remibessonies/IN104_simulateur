
from distutils.core import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="simulateur.cpp.gameState",
        sources=["simulateur/cpp/gameState.pyx"],
        include_dirs = ["."], 
        #extra_compile_args=["-std=c++11"],
        #extra_link_args=["-std=c++11"]
    ),
    Extension(
        name="simulateur.cpp.boardState",
        sources=["simulateur/cpp/boardState.pyx"],
        include_dirs = ["."], 
        #extra_compile_args=["-std=c++11"],
        #extra_link_args=["-std=c++11"]
    ),
    Extension(
        name="simulateur.cpp.move",
        sources=["simulateur/cpp/move.pyx"],
        include_dirs = ["."], 
        #extra_compile_args=["-std=c++11"],
        #extra_link_args=["-std=c++11"]
    )
]

setup(
    ext_modules = cythonize(extensions)
)

'''
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = "IN104_simulateur",
    ext_modules = cythonize('code/cpp/*.pyx'),
)
'''
