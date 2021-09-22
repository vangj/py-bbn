# Cython

Build the wheel.

```bash
make build-dist
```

Create conda environment.

```bash
conda create -y -n pybbn python=3.8
conda activate pybbn
pip install -r requirements.txt
pip install dist/*.whl
```

Run.

```bash
python docs/source/code/ace-demo.py 
python docs/source/code/api-generation.py
```