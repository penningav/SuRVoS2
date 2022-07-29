

import numpy as np
from loguru import logger
from qtpy import QtWidgets
from survos2.model import DataModel
from survos2.frontend.components.base import LineEdit
from survos2.frontend.plugins.pipeline.base import PipelineCardBase

class RasterizePoints(PipelineCardBase):
    def __init__(self,fid, ftype, fname, fparams, parent=None):
        super().__init__(
            fid=fid,
            ftype=ftype,
            fname=fname,
            fparams=fparams
        )
    def setup(self):
        self._add_annotations_source()
        self._add_feature_source()
        self._add_objects_source()
    def compute_pipeline(self):
        src = DataModel.g.dataset_uri(self.feature_source.value(), group="features")
        all_params = dict(src=src, modal=True)
        all_params["workspace"] = DataModel.g.current_workspace
        all_params["feature_id"] = self.feature_source.value()
        all_params["object_id"] = str(self.objects_source.value())
        all_params["acwe"] = self.widgets["acwe"].value()
        all_params["dst"] = self.dst
        return all_params
