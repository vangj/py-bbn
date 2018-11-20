# Information

To run these Jupyter notebooks, you will need to create a conda environment with py-bbn installed.

```bash
conda create -n py-bbn python=2.7
source activate py-bbn
pip install py-bbn
python -m ipykernel install --user --name py-bbn --display-name "py-bbn"
```

Make sure you install [graphviz](http://www.graphviz.org/). On Mac, you may [type in](https://brewformulas.org/Graphviz) the following.

```bash
brew install graphviz
```

Then you can start Jupyter as follows.

```bash
jupyter notebook
```