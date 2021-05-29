from setuptools import setup, Extension

setup(
    name="mykmeanssp",
    version="0.1.0",
    description="Our kmeans code",
    py_modules=["kmeans_pp"],
    package_dir={'':'src'},
    packages=find_packages(),
    
    ext_modules=[
        Extension(
            'mykmeanssp',
            sources = ['kmeans.c'],
            )
        ]
)

