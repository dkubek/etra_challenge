# -*- coding: utf-8 -*-
import sys
import urllib.request
from pathlib import Path
from typing import Union
from zipfile import ZipFile

import pandas as pd
import numpy as np
import remodnav

SCREEN_SIZE = (40, 30)  # cm x cm
SCREEN_RESOLUTION = (1024, 768)  # px x px
VIEWING_DISTANCE = 57  # cm
SAMPLING_RATE = 500  # Hz


class ETRA:
    """
    ETRA Dataset
    """

    data_dir: Path = None

    # URL to ETRA Dataset
    _URL = "http://smc.neuralcorrelate.com/ETRA2019/ETRA2019Challenge.zip"

    def __init__(self, data_dir: str = "data", dataset: str = "etra") -> None:
        self.data_dir = Path.cwd() / data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

        data_path = self.data_dir / "{}.zip".format(dataset)
        if not data_path.exists():
            print(
                f"Downloading dataset {dataset} (this can take a while) ... ",
                file=sys.stderr,
                end="",
            )
            urllib.request.urlretrieve(self._URL, filename=data_path)
            print("DONE", file=sys.stderr)
        else:
            print(f"Dataset {dataset} already downloaded.", file=sys.stderr)

        with ZipFile(data_path, "r") as archive:
            print(f"Unpacking {dataset}...", file=sys.stderr)
            for filename in archive.namelist():
                file_path = self.data_dir / filename
                if not file_path.exists():
                    print(f"Extracting\t{filename}", file=sys.stderr)
                    archive.extract(filename, path=self.data_dir)


def read_data(data_path: Union[str, Path]) -> pd.DataFrame:
    data_path = Path(data_path)

    filename = data_path.stem
    (
        participant_id,
        trial_id,
        fv_fixation,
        task_type,
        stimulus_id,
    ) = filename.split("_")[:5]

    df = pd.read_csv(data_path)
    orig_cols = df.columns.to_list()
    new_cols = {
        "participant_id": participant_id,
        "trial_id": trial_id,
        "fv_fixation": fv_fixation,
        "task_type": task_type,
        "stimulus_id": stimulus_id if stimulus_id else pd.NA,
    }
    df = df.assign(**new_cols)
    df = df[
        [
            "participant_id",
            "trial_id",
            "fv_fixation",
            "task_type",
            "stimulus_id",
        ]
        + orig_cols
    ]

    return df


def _get_default_classifier():
    px2deg = remodnav.clf.deg_per_pixel(
        SCREEN_SIZE[0], VIEWING_DISTANCE, SCREEN_RESOLUTION[0]
    )
    clf = remodnav.EyegazeClassifier(
        px2deg=px2deg, sampling_rate=SAMPLING_RATE
    )
    return clf


def _detect(data):
    clf = _get_default_classifier()

    tmp = data[["x", "y"]].fillna(method="ffill")
    dt = {"names": ["x", "y"], "formats": [float, float]}
    hlp = np.zeros(len(tmp), dtype=dt)
    hlp["x"] = tmp.x.values
    hlp["y"] = tmp.y.values

    pp = clf.preproc(hlp, max_vel=1500)

    events = clf(pp, classify_isp=True, sort_events=True)

    return hlp, pp, events


def detect(data):
    _, _, events = _detect(data)
    events = pd.DataFrame(
        events,
        columns=[
            "label",
            "start_time",
            "end_time",
            "start_x",
            "start_y",
            "end_x",
            "end_y",
            "amp",
            "peak_vel",
            "med_vel",
            "avg_vel",
        ],
    )
    events[["start_time", "end_time"]] *= 1000
    events = events.astype({"start_time": int, "end_time": int})

    return events


def show_gaze(data):
    clf = _get_default_classifier()
    data, pp, events = _detect(data)
    clf.show_gaze(data=data, pp=pp, events=events)