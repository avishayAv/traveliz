from dataclasses import dataclass


@dataclass
class GetLocationHyperParams:
    prev_word_decrease: float = 0.05
    tel_aviv_priority: float = 0.01
    similarity_th: float = 0.85


get_location_hyper_params = GetLocationHyperParams()
