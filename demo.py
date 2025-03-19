if __name__ == '__main__':
    import os
    import time
    t = time.time()
    import sys
    from PyQt6.QtCore import Qt, QTranslator
    from PyQt6.QtWidgets import QApplication
    from qfluentwidgets import FluentTranslator
    # from qfluentwidgets import FluentIcon as FIF
    from app.common.config import cfg
    from app.view.main_window import MainWindow
    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)


    
    t0 = time.time()
    print(t0-t)
    # create main window
    w = MainWindow()
    # w.show()
    
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