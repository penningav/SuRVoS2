

import numpy as np
from loguru import logger
from qtpy import QtWidgets
from survos2.model import DataModel
from survos2.frontend.components.base import LineEdit, ComboBox, HWidgets
from survos2.frontend.plugins.pipeline.base import PipelineCardBase

class Train3DCNN(PipelineCardBase):
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
        self._add_fcn_choice()
    def compute_pipeline(self):
        src = DataModel.g.dataset_uri(self.feature_source.value(), group="features")
        all_params = dict(src=src, dst=self.dst, modal=True)
        all_params["workspace"] = DataModel.g.current_workspace
        all_params["feature_id"] = str(self.feature_source.value())
        all_params["anno_id"] = str(self.annotations_source.value().rsplit("/", 1)[-1])
        if self.objects_source.value() != None:
            all_params["objects_id"] = str(self.objects_source.value().rsplit("/", 1)[-1])
            #all_params["objects_id"] = str(self.objects_source.value()
            print(all_params["objects_id"])
        else:
            #     all_params["objects_id"] = str(self.objects_source.value())
            all_params["objects_id"] = "None"
        all_params["fpn_train_params"] = {}
        all_params["fcn_type"] = self.fcn_type.value()
        
        return all_params

class Predict3DCNN(PipelineCardBase):
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
        self._add_fcn_choice()
    def compute_pipeline(self):
        src = DataModel.g.dataset_uri(
            self.feature_source.value(), group="features"
        )
        all_params = dict(src=src, modal=True)
        all_params["workspace"] = DataModel.g.current_workspace
        all_params["anno_id"] = str(self.annotations_source.value().rsplit("/", 1)[-1])
        all_params["feature_id"] = self.feature_source.value()
        all_params["model_fullname"] = self.model_fullname
        all_params["model_type"] = self.model_type.value()
        all_params["dst"] = self.dst
        all_params["overlap_mode"] = self.overlap_type.value()
        
        return all_params

