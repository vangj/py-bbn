from setuptools import setup, find_packages

with open('README.rst', 'r') as fh:
    long_desc = fh.read()

setup(
    name='pybbn',
    version='1.0.7',
    author='Jee Vang',
    author_email='vangjee@gmail.com',
    packages=find_packages(),
    description='Learning and Inference in Bayesian Belief Networks',
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    url='https://github.com/vangj/py-bbn',
    keywords=' '.join(['bayesian', 'belief', 'network', 'exact', 'approximate', 'inference', 'junction', 'tree',
                       'algorithm', 'pptc', 'dag', 'gibbs', 'sampling', 'multivariate', 'conditional', 'gaussian',
                       'linear', 'causal', 'causality', 'structure', 'parameter']),
    install_requires=['numpy', 'scipy', 'networkx', 'pandas', 'matplotlib', 'pygraphviz'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Development Status :: 5 - Production/Stable'
    ],
    include_package_data=True
)
