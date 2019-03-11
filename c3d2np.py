from pathlib import Path
from c3d import Reader
import argparse
import numpy as np
from tqdm import tqdm

MARKERS = ['C7', 'LA', 'RA', 'REP', 'LEP', 'RUL', 'LUL', 'RASIS', 'LASIS', 'RPSIS', 'LPSIS', 'RGT', 'LGT', 'RLE',
           'LLE', 'RCA', 'LCA', 'RFM', 'LFM']

if __name__ == '__main__':
    """
    DATASET PATH IS STRUCTURED AS:    
        ARGS.DATASET_PATH/
        ├── 0/    # CLASS
        |    ├────0/   # SUBJECT
        |    └────1/   # SUBJECT
        |    
        ├── 1/    # CLASS   
        ├── 2/    # CLASS
        └── 3/    # CLASS 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_path', type=Path, help='Dataset directory')
    parser.add_argument('--dump_path', type=Path, default='/tmp/diplegia', help='Dump directory')
    args = parser.parse_args()

    dataset_path: Path = args.dataset_path
    dump_path: Path = args.dump_path
    dump_path.mkdir(exist_ok=True)

    c3d_paths = sorted(dataset_path.glob('**/*.c3d'))
    for c3d_path in tqdm(c3d_paths, 'iterating .c3d'):
        reader = Reader(open(c3d_path, 'rb'))
        # read number of valid frames as declared in the header
        lf = reader.last_frame()
        ff = reader.first_frame()
        num_frames = lf - ff
        # read markers
        markers = [i.strip() for i in reader.get('POINT').get('LABELS').string_array]

        # prepare a zero buffer
        X = np.zeros((num_frames, len(MARKERS), 4))
        X[:, -1] = -1  # set everything to invalid
        for i, points, analog in reader.read_frames():
            # we MUST check i
            if i < ff:
                continue
            if i >= lf:
                break
            i -= ff  # np row index
            # iterate over the point and the marker set of the file
            for p, marker in zip(points, markers):
                try:
                    j = MARKERS.index(marker)  # np col index
                    X[i, j] = p[0:4]
                except ValueError:
                    continue
        # write the same hierarchy of the input in dump_path
        example_path = dump_path / c3d_path.parents[1].name / c3d_path.parents[0].name
        example_path.mkdir(exist_ok=True, parents=True)
        np.save(example_path / f'{c3d_path.stem}.npy', X)
