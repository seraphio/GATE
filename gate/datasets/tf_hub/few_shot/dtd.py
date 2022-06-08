import pathlib
from typing import List, Optional, Union, Any

from dotted_dict import DottedDict
from omegaconf import DictConfig

from gate.base.utils.loggers import get_logger
from gate.configs.datasets.data_splits_config import data_splits_dict
from gate.datasets.data_utils import (
    FewShotSuperSplitSetOptions,
)
from gate.datasets.tf_hub import bytes_to_string
from gate.datasets.tf_hub.few_shot.base import (
    FewShotClassificationDatasetTFDS,
)

log = get_logger(
    __name__,
)


# TODO ensure the multi-set few-shot dataset splits things
# into support/val/query for
# consistency Make sure the two datasets have matching sets
# for consistency again
# Create one few-shot dataset for each of the metadataset datasets
# class DTDClassificationDataset(ClassificationDataset):
#     def __init__(
#         self,
#         dataset_root: Union[str, pathlib.Path],
#         split_name: str,
#         download: bool,
#         input_transform: Optional[Any] = None,
#         target_transform: Optional[Any] = None,
#     ):
#         DATASET_NAME = "caltech_birds2011"
#         super(ClassificationDataset, self).__init__(
#             dataset_name=DATASET_NAME,
#             input_target_keys={"input": "image", "target": "label"},
#             dataset_root=dataset_root,
#             split_name=split_name,
#             download=download,
#             input_transform=input_transform,
#             target_transform=target_transform,
#         )


class DTDFewShotClassificationDataset(FewShotClassificationDatasetTFDS):
    def __init__(
        self,
        dataset_root: Union[str, pathlib.Path],
        split_name: str,
        download: bool,
        num_episodes: int,
        min_num_classes_per_set: int,
        min_num_samples_per_class: int,
        num_classes_per_set: Union[int, List[int]],  # n_way
        num_samples_per_class: Union[int, List[int]],  # n_shot
        variable_num_samples_per_class: bool,
        variable_num_classes_per_set: bool,
        support_set_input_transform: Optional[Any],
        query_set_input_transform: Optional[Any],
        support_set_target_transform: Optional[Any] = None,
        query_set_target_transform: Optional[Any] = None,
        support_to_query_ratio: float = 0.75,
        rescan_cache: bool = True,
    ):
        DATASET_NAME = "dtd"
        super(DTDFewShotClassificationDataset, self).__init__(
            modality_config=DottedDict(image=True),
            input_shape_dict=DottedDict(
                image=dict(channels=3, height=84, width=84)
            ),
            dataset_name=DATASET_NAME,
            dataset_root=dataset_root,
            split_name=split_name,
            download=download,
            num_episodes=num_episodes,
            num_classes_per_set=num_classes_per_set,
            num_samples_per_class=num_samples_per_class,
            variable_num_samples_per_class=variable_num_samples_per_class,
            variable_num_classes_per_set=variable_num_classes_per_set,
            support_to_query_ratio=support_to_query_ratio,
            rescan_cache=rescan_cache,
            input_target_annotation_keys=dict(
                inputs="image",
                targets="label",
                target_annotations="file_name",
            ),
            support_set_input_transform=support_set_input_transform,
            query_set_input_transform=query_set_input_transform,
            support_set_target_transform=support_set_target_transform,
            query_set_target_transform=query_set_target_transform,
            split_percentage={
                FewShotSuperSplitSetOptions.TRAIN: 33,
                FewShotSuperSplitSetOptions.VAL: 7,
                FewShotSuperSplitSetOptions.TEST: 7,
            },
            split_config=DictConfig(data_splits_dict[DATASET_NAME]),
            label_extractor_fn=lambda x: bytes_to_string(x).split("/")[0],
            min_num_classes_per_set=min_num_classes_per_set,
            min_num_samples_per_class=min_num_samples_per_class,
        )
