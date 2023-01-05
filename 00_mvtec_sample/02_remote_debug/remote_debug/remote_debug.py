"""
************************************************************
remote_debug.py - HDevEngine example for HALCON/Python
************************************************************

Project: HALCON/Python
Description:
Example for debugging HDevelop procedure running as part of Python application,
from HDevelop.

************************************************************

(c) 1996-2022 by MVTec Software GmbH

Software by: MVTec Software GmbH, www.mvtec.com
"""

import os
import sys

import halcon as ha


def setup_hdev_engine():
    """Setup HDevEngine by setting procedure search paths."""
    # example_dir = ha.get_system_s('example_dir')
    example_dir = '.'
    hdev_example_dir = os.path.join(example_dir, 'hdevengine')

    engine = ha.HDevEngine()
    engine.set_procedure_path(os.path.join(hdev_example_dir, 'procedures'))

    engine.set_attribute('debug_port', 57786)

    engine.start_debug_server()

    return engine


if __name__ == '__main__':
    engine = setup_hdev_engine()

    proc = ha.HDevProcedure.load_external('count_nuts')

    proc_call = ha.HDevProcedureCall(proc)
    # Signal that execute should wait for the debug session.
    proc_call.wait_for_debug_connection()

    # img = ha.read_image('rings_and_nuts')
    img = ha.read_image('image/rings_and_nuts')
    proc_call.set_input_iconic_param_by_name('Image', img)

    debug_port = engine.get_attribute('debug_port')
    print(f'Open HDevelop and \'Execute/Attach to Process\' on port {debug_port}')
    sys.stdout.flush()

    proc_call.execute()

    print('Debugging done.')

    num_objects = proc_call.get_output_control_param_by_name('NumObjects')[0]
    print(f'NumObjects: {num_objects}')

    assert num_objects == 8
