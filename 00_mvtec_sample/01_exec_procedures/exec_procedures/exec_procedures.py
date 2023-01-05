"""
************************************************************
exec_procedures.py - HDevEngine example for HALCON/Python
************************************************************

Project: HALCON/Python
Description:
Example for executing local and external HDevelop procedures.

Note, HDevEngine is a mutable singleton.

************************************************************

(c) 1996-2022 by MVTec Software GmbH

Software by: MVTec Software GmbH, www.mvtec.com
"""

import os

import halcon as ha


def open_window(width, height, row, col):
    """Open native window for drawing."""
    if os.name == 'nt':
        # Windows applications wanting to perform GUI tasks, require an
        # application level event loop. By default console applications like
        # this do not have one, but HALCON can take care of this for us,
        # if we enable it by setting this system parameter.
        ha.set_system('use_window_thread', 'true')

    return ha.open_window(
        row=row,
        column=col,
        width=width,
        height=height,
        father_window=0,
        mode='visible',
        machine=''
    )


def setup_hdev_engine():
    """Setup HDevEngine by setting procedure search paths."""
    # example_dir = ha.get_system_s('example_dir')
    example_dir = '.'
    hdev_example_dir = os.path.join(example_dir, 'hdevengine')

    engine = ha.HDevEngine()
    engine.set_procedure_path(os.path.join(hdev_example_dir, 'procedures'))

    return hdev_example_dir


def init_acq_handle(program):
    """Execute procedure for image acquisition."""
    proc = ha.HDevProcedure.load_local(program, 'init_acquisition')
    proc_call = ha.HDevProcedureCall(proc)
    proc_call.execute()
    return proc_call.get_output_control_param_by_name('AcqHandle')


def display_fin(window, fin_region, fin_area):
    """Draw fin region and info into window"""
    ha.set_color(window, 'red')
    ha.set_draw(window, 'margin')
    ha.disp_obj(fin_region, window)

    ha.set_color(window, 'white')
    ha.set_tposition(window, 150, 20)
    ha.write_string(window, f'Fin Area: {fin_area[0]}')


def zoom_in_on_fin(img, fin_region):
    """Display zoomed in fin region in new window."""
    zoom_scale = 2
    margin = 5

    _, center_row, center_col = ha.area_center_s(fin_region)
    row1, col1, row2, col2 = ha.smallest_rectangle1_s(fin_region)

    region_height = row2 - row1
    region_width = col2 - col1

    zoom_window = open_window(
        width=(region_width + (2 * margin)) * zoom_scale,
        height=(region_height + (2 * margin)) * zoom_scale,
        row=100 + (center_row / 2),
        col=100 + ((center_col / 2) + 30)
    )
    ha.set_part(
        zoom_window,
        row1 - margin,
        col1 - margin,
        row2 - margin,
        col2 - margin
    )
    ha.disp_obj(img, zoom_window)
    ha.set_color(zoom_window, 'red')
    ha.disp_obj(fin_region, zoom_window)

    # Keep the window alive in caller.
    return zoom_window


if __name__ == '__main__':
    hdev_example_dir = setup_hdev_engine()

    program = ha.HDevProgram(
        os.path.join(hdev_example_dir, 'hdevelop', 'fin_detection.hdev')
    )

    proc = ha.HDevProcedure.load_local(program, 'detect_fin')
    proc_call = ha.HDevProcedureCall(proc)

    acq_handle = init_acq_handle(program)

    for _ in range(3):
        acq_img = ha.grab_image(acq_handle)
        width, height = ha.get_image_size_s(acq_img)

        window = open_window(width, height, row=100, col=100)
        ha.disp_obj(acq_img, window)

        proc_call.set_input_iconic_param_by_name('Image', acq_img)
        proc_call.execute()
        fin_region = proc_call.get_output_iconic_param_by_name('FinRegion')
        fin_area = proc_call.get_output_control_param_by_name('FinArea')

        display_fin(window, fin_region, fin_area)
        input('Press Enter to continue...')

        zoom_window = zoom_in_on_fin(acq_img, fin_region)
        input('Press Enter to continue...')
