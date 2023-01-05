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
    example_dir = '../'
    hdev_example_dir = os.path.join(example_dir, 'hdevelop')

    return hdev_example_dir


def execute_hdev_main(program):
    # ファイルシステムからプロシージャーをロードしてHDevProcedureインスタンスを初期化する。
    proc = ha.HDevProcedure.load_local(program, 'main_processing')
    # HDevProcedureインスタンスから特定のHDevProcedureCallインスタンスを生成する。
    proc_call = ha.HDevProcedureCall(proc)
    # 実行
    proc_call.execute()
    
    return proc_call


def display_image_and_xld(window, image, xld, point):
    #　画像
    ha.disp_obj(image, window)
    
    #　XLD
    ha.set_color(window, 'red')
    ha.set_draw(window, 'margin')
    ha.disp_obj(xld, window)
    
    #　四角形の中心座標
    ha.set_color(window, 'white')
    ha.set_tposition(window, 150, 20)
    ha.write_string(window, f'Fin Area: {point[0], point[1]}')

if __name__ == '__main__':
    # .hdevファイルパスの初期設定
    hdev_example_dir = setup_hdev_engine()

    # .hdevファイル名の指定
    program = ha.HDevProgram(
        os.path.join(hdev_example_dir, 'test_hdev.hdev')
    )
    
    #　実行後のHDevProcedureCallインスタンスを取得
    proc_call = execute_hdev_main(program)
    
    #　proc_callから出力変数を取得
    image = proc_call.get_output_iconic_param_by_name('image')
    image_result = proc_call.get_output_iconic_param_by_name('image_result')
    center_xld = proc_call.get_output_iconic_param_by_name('center_xld')
    center_point = proc_call.get_output_control_param_by_name('center_point')
    
    #　画像サイズを取得
    width, height = ha.get_image_size_s(image)
    
    #　ウィンドウに画像を表示
    window = open_window(width, height, row=100, col=100)
    ha.disp_obj(image, window)
    input('Press Enter to continue...')
    ha.clear_window(window)
    
    #　処理結果を表示
    display_image_and_xld(window, image_result, center_xld, center_point)
    input('Press Enter to continue...')
