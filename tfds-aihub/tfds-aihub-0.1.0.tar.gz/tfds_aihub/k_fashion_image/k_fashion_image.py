"""k_fashion_image dataset."""
import os
import zipfile
import json

import numpy as np
import tensorflow_datasets as tfds
from PIL import Image, ImageDraw

# TODO(k_fashion_image): Markdown description  that will appear on the catalog page.
_DESCRIPTION = """
coord: top left
"""

# TODO(k_fashion_image): BibTeX citation
_CITATION = """
"""


_CLASS_LIST = [
    ["트래디셔널", ["클래식", "프레피"]],
    ["매니시", ["매니시", "톰보이"]],
    ["페미닌", ["페미닌", "로맨틱", "섹시"]],
    ["에스닉", ["히피", "웨스턴", "오리엔탈"]],
    ["컨템포러리", ["모던", "소피스트케이티드", "아방가르드"]],
    ["내추럴", ["컨트리", "리조트"]],
    ["젠더플루이드", ['젠더리스']],
    ["스포티", ["스포티"]],
    ["서브컬쳐", ["레트로", "키치/키덜트", "힙합", "펑크"]],
    ["캐주얼", ["밀리터리", "스트리트"]],
    ["UNKNOWN", ["UNKNOWN"]],
]
_CLASS_MAP = dict(_CLASS_LIST)

_CORASE_STYLE_NAMES = [item_tuple[0] for item_tuple in _CLASS_LIST]
_FINE_STYLE_NAMES = [item for item_tuple in _CLASS_LIST for item in item_tuple[1]]

_BBOX_TYPE = ["아우터", "상의", "하의", "원피스"]


class KFashionImage(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for k_fashion_image dataset."""
    MANUAL_DOWNLOAD_INSTRUCTIONS = """
    <https://aihub.or.kr/aidata/7988/download> 에서 다운로드 받은 뒤 manual download dir에 위치시켜 주시기 바랍니다.

    접근 경로: "dl_manager.manual_dir / 'K-Fashion 이미지'
    """

    VERSION = tfds.core.Version("1.1.0")
    RELEASE_NOTES = {
        "1.1.0": "Initial release.",
    }

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        # TODO(k_fashion_image): Specifies the tfds.core.DatasetInfo object
        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION,
            features=tfds.features.FeaturesDict(
                {
                    "image": tfds.features.Image(shape=(None, None, 3)),
                    "objects": tfds.features.Sequence({
                        "type": tfds.features.ClassLabel(names=_BBOX_TYPE),
                        "bbox": tfds.features.BBoxFeature(),
                        "segmentation_mask": tfds.features.Image(shape=(None, None, 1)),
                    })
                    # TODO style 관련 정보
                }
            ),
            supervised_keys=None,
            homepage="https://aihub.or.kr/aidata/7988",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""
        path = dl_manager.manual_dir / 'K-Fashion 이미지'

        return {
            "Training": self._generate_examples(path / "Training"),
            "Validation": self._generate_examples(path / "Validation"),
        }

    def _generate_examples(self, path):
        """Yields examples."""
        labeling_zipfile = zipfile.ZipFile(path / "라벨링데이터.zip", "r")
        for image_path in path.glob("원천데이터*.zip"):
            with zipfile.ZipFile(path / image_path, "r") as image_zipfile:
                for item in image_zipfile.infolist():
                    # skip directory item
                    if item.is_dir():
                        continue

                    with image_zipfile.open(item.filename) as img_file:
                        image_bytes = img_file.read()

                    basename, _ = os.path.splitext(item.filename)
                    with labeling_zipfile.open(basename + ".json", "r") as metafile:
                        metadata = json.loads(metafile.read().decode('utf8'))
                        height = metadata['이미지 정보']['이미지 높이']
                        width = metadata['이미지 정보']['이미지 너비']
                        metadata = metadata["데이터셋 정보"]["데이터셋 상세설명"]

                    yield str(item.filename), {
                        "image": image_bytes,
                        "objects": _dict_to_bbox(metadata['렉트좌표'], metadata['폴리곤좌표'], width, height),
                    }

        labeling_zipfile.close()


def _dict_to_bbox(rect_coord, polygon_coord, width, height):
    results = []
    for key in rect_coord.keys():
        rect_item = rect_coord[key]
        polygon_item = polygon_coord[key]

        assert len(rect_item) == 1
        if len(rect_item[0].keys()) == 0:
            continue

        results.append(
            {
                "type": key,
                "bbox": tfds.features.BBox(
                    xmin=_trim_scale((rect_item[0]["X좌표"]) / width),
                    xmax=_trim_scale((rect_item[0]["X좌표"] + rect_item[0]["가로"]) / width),
                    ymin=_trim_scale((rect_item[0]["Y좌표"]) / height),
                    ymax=_trim_scale((rect_item[0]["Y좌표"] + rect_item[0]["세로"]) / height),
                ),
                "segmentation_mask": _draw_polygon(_aihub_coord_to_coord(polygon_item[0]), width, height)
            }
        )

    return results


def _trim_scale(x):
    return max(min(x, 1.0), 0.0)


def _draw_polygon(coords, width, height):
    img = Image.new('L', (width, height), 0)
    ImageDraw.Draw(img).polygon(coords, outline=2, fill=1)
    mask = np.array(img).reshape([width, height, 1])
    return mask


def _aihub_coord_to_coord(coords):
    """Covert aihub-style coords to standard format.

    >>> _aihub_coord_to_coord({
    ...   "X좌표1": 602.004,
    ...   "X좌표2": 571.004,
    ...   "X좌표3": 545.004,
    ...   "X좌표4": 531.004,
    ...   "Y좌표1": 520.004,
    ...   "Y좌표2": 505.004,
    ...   "Y좌표3": 465.004,
    ...   "Y좌표4": 428.004,
    ... })
    [(602.004, 520.004), (571.004, 505.004), (545.004, 465.004), (531.004, 428.004)]
    """
    max_num = max(int(item[3:]) for item in coords)
    return [(coords[f'X좌표{n}'], coords[f'Y좌표{n}']) for n in range(1, max_num + 1) if f'X좌표{n}' in coords]
