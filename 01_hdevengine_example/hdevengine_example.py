import os

import halcon as ha

if __name__ == '__main__':
    example_dir = ha.get_system_s('example_dir')
    procedure_path = os.path.join(example_dir, 'hdevengine', 'procedures')
    
    hdev_engine = ha.HDevEngine()
    hdev_engine.set_procedure_path(procedure_path)

    img = ha.read_image('fin2')

    procedure = ha.HDevProcedure.load_external('detect_fin')
    proc_call = ha.HDevProcedureCall(procedure)
    
    proc_call.set_input_iconic_param_by_name('Image', img)
    proc_call.execute()

    fin_area = proc_call.get_output_control_param_by_name('FinArea')[0]
    print(f'Fin Area: {fin_area}')