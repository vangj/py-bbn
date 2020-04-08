import argparse
import json
import sys
import time

from pybbn.graph.dag import Bbn
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.pptc.inferencecontroller import InferenceController


def get_bbn(fpath):
    with open(fpath, 'r') as f:
        start = time.time()
        bbn = Bbn.from_dict(json.loads(f.read())) if fpath.endswith('.json') else Bbn.from_csv(fpath)
        stop = time.time()
        diff = stop - start
        print(f'{diff:.5f} : load time')

        start = time.time()
        jt = InferenceController.apply(bbn)
        stop = time.time()
        diff = stop - start
        print(f'{diff:.5f} : inference time')

        return bbn, jt


def parse_args(args):
    parser = argparse.ArgumentParser('Query BBN')
    parser.add_argument('-f', '--file', help='path to file')
    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    bbn, jt = get_bbn(args.file)

    while True:
        value = input(f'command ')
        if value == 'q':
            break
        elif value == 'p':
            posteriors = jt.get_posteriors()
            for name, d in posteriors.items():
                s = name + ' ' + ' '.join([f'{k}={v:.5f}' for k, v in d.items()])
                print(s)
        elif value == 'c':
            jt.unobserve_all()
        else:
            name, val = value.split('=')

            ev = EvidenceBuilder() \
                .with_node(jt.get_bbn_node_by_name(name)) \
                .with_evidence(val, 1.0) \
                .build()

            start = time.time()
            jt.set_observation(ev)
            stop = time.time()
            diff = stop - start
            print(f'{diff:.5f} : inference time')
    print('finished')
