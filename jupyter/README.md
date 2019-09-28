# Information

To run these Jupyter notebooks, you will need to create a conda environment with py-bbn installed.

```bash
conda create -n py-bbn python=2.7
source activate py-bbn
pip install py-bbn
python -m ipykernel install --user --name py-bbn --display-name "py-bbn"
```

Make sure you install [graphviz](http://www.graphviz.org/). 
On Mac, you may [type in](https://brewformulas.org/Graphviz) `brew install graphviz`.
On Ubuntu you may type in `sudo apt install python-pydot python-pydot-ng graphviz`.

Then you can start Jupyter as follows.

```bash
jupyter notebook
```

# View the notebooks

View the notebooks online.

* [exact-inference.ipynb](https://nbviewer.jupyter.org/github/vangj/py-bbn/blob/master/jupyter/exact-inference.ipynb?flush_cache=true) shows how to build a BBN and do exact inference
* [exact-inference-evidences.ipynb](https://nbviewer.jupyter.org/github/vangj/py-bbn/blob/master/jupyter/exact-inference-evidences.ipynb?flush_cache=true) shows how to build a BBN and do exact inference with evidences
* [approximate-inference.ipynb](https://nbviewer.jupyter.org/github/vangj/py-bbn/blob/master/jupyter/approximate-inference.ipynb?flush_cache=true) shows how to do approximate inference
* [approximate-inference-different-structures.ipynb](https://nbviewer.jupyter.org/github/vangj/py-bbn/blob/master/jupyter/approximate-inference-different-structures.ipynb?flush_cache=true) shows how to do approximate inference with different structures
* [generate-bbn.ipynb](https://nbviewer.jupyter.org/github/vangj/py-bbn/blob/master/jupyter/generate-bbn.ipynb?flush_cache=true) shows how to generate different BBNs randomly
* [some-features.ipynb](https://nbviewer.jupyter.org/github/vangj/py-bbn/blob/master/jupyter/some-features.ipynb?flush_cache=true) shows some extra features of the py-bbn API