if __name__ == '__main__':
    import os
    import json
    import sys
    from PyQt6.QtCore import Qt, QTranslator
    from PyQt6.QtWidgets import QApplication
    from qfluentwidgets import FluentTranslator
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
    if not os.path.exists(os.path.join('data', 'cache')):
        os.makedirs(os.path.join('data', 'cache'), exist_ok=True)

    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)
    clientTranslator = QTranslator()
    clientTranslator.load(locale, 'client', '.', 'app/resource/i18n')
    app.installTranslator(translator)
    app.installTranslator(clientTranslator)
    
    w = MainWindow()

    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    
    app.exec()