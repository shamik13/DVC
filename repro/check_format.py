class ReproCheckFormat:

    """
    Chweck the format of a raw dataset
    """

    def check_format(self):
        self._check_data_structure()
        self._check_product_id()
        self._check_label_name()
        self._check_flag_name()
        self._check_camera_angle()

    def _check_naming_convention(self):

        """
        [0-9]+_[0-9]{4}_[0-9]{4}_[0-9]{8}
        """
        pass

    def _check_data_structure(self):

        """
        ├── color_images
        |   ├── *.bmp
        |   └── *.jpg
        ├── color_images
        |   ├── *.bmp
        |   └── *.jpg
        ├── jsons
        |   └── *.json
        └── markings
            └── *.bmp
        """
        pass

    def _check_product_id(self):
        pass

    def _check_label_name(self):
        pass

    def _check_flag_name(self):
        pass

    def _check_camera_angle(self):
        pass

    def _exit_process(self):
        pass
