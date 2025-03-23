if __name__ == '__main__':
    import os
    import time
    import json
    t = time.time()
    import sys
    from PyQt6.QtCore import Qt, QTranslator
    from PyQt6.QtWidgets import QApplication
    from qfluentwidgets import FluentTranslator
    # from qfluentwidgets import FluentIcon as FIF
    from app.common.config import cfg
    from app.view.main_window import MainWindow


    def check_data_directory(base, structure):
        for name, content in structure.items():
            path = os.path.join(base, name)
            if content is None:
                if not os.path.exists(path):
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, 'w', encoding='utf-8') as file:
                        json.dump({}, file)
            else:
                check_data_directory(path, content)

    file_structure = {
        'data': {
            'courseAnnouncement.json': None,
            'courseAssignments.json': None,
            'courseContent.json': None,
            'courseGrade.json': None,
            'courseInfo.json': None,
            'courseList.json': None,
            'courseVideoList.json': None,
            'login.json': None,
            'portal.json': None
        }
    }
    check_data_directory('', file_structure)
    if not os.path.exists('download'):
        os.makedirs('download', exist_ok=True)
    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    t0 = time.time()
    print(t0-t)
    # create main window
    w = MainWindow()
    t1 = time.time()
    print(t1-t0)
    # enable dpi scale
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))
    # internationalization
    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)
    galleryTranslator = QTranslator()
    galleryTranslator.load(locale, 'calculator', '.', 'app/resource/i18n')

    app.installTranslator(translator)
    app.installTranslator(galleryTranslator)
    t2 = time.time()
    print(t2-t1)
    app.exec()