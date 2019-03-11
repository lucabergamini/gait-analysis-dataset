from open3d import *
import argparse
import numpy as np
from pathlib import Path

global joints
global X
global row_idx
global dump_path


class Joint(object):
    def __init__(self, mesh, location):
        self.location = np.asarray([0, 0, 0])
        self.mesh = mesh
        self.move_to_point(location)

    def move_to_point(self, location):
        translation = (location - self.location).reshape(3, 1)
        rotation = np.eye(3)
        last_row = np.asarray([0, 0, 0, 1]).reshape(1, 4)
        m = np.concatenate([rotation, translation], 1)
        m = np.concatenate([m, last_row], 0)
        self.mesh.transform(m)
        self.location = location


def init_geometries(X: np.ndarray):
    joints = []
    for marker_index in range(X.shape[1]):
        location = X[0, marker_index, :-1]
        joint = Joint(create_mesh_sphere(radius=0.025), location)
        joint.mesh.paint_uniform_color(np.random.rand(3))
        joints.append(joint)
    return joints


def f(vis):
    global row_idx, X, joints

    vis.get_render_option().background_color = (0, 0, 0)
    vis.get_render_option().light_on = False
    # update geometries
    for i, marker in enumerate(X[row_idx]):
        location = marker[:-1]
        joints[i].move_to_point(location)

    if row_idx < len(X) - 1:
        row_idx += 1

    vis.update_geometry()
    # if row_idx % 5 == 0:
    #     render = np.asarray(vis.capture_screen_float_buffer(do_render=True))
    #     render = (render * 255).astype(np.uint8)
    #     render = cv2.cvtColor(render, cv2.COLOR_RGB2BGR)
    #     cv2.imwrite(str(dump_path / f'{row_idx:03d}.jpg'), render)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('npy_path', type=Path, help='.npy file path')
    args = parser.parse_args()

    # dump_path = Path('/tmp/dump_video/') / args.npy_path.stem
    # dump_path.mkdir(exist_ok=True, parents=True)

    X = np.load(args.npy_path)
    X[..., :-1] /= 1000  # open3D assume metric units
    # set time to 0
    row_idx = 0
    # init a sphere for each joint
    joints = init_geometries(X)
    # add a ref system
    floor = create_mesh_box(width=10, height=10, depth=0.01)
    floor.vertices = Vector3dVector(np.asarray(floor.vertices) - [5, 5, 0])
    floor.paint_uniform_color([0.5, 0, 0])
    floor.compute_vertex_normals()

    draw_geometries_with_animation_callback([j.mesh for j in joints] + [floor], f,
                                            width=960, height=540)
