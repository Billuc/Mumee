from vcr import VCR


def generate_vcr(folder: str = None):
    return VCR(
        path_transformer=VCR.ensure_suffix(".yml"),
        cassette_library_dir=f"tests/cassettes{'/' + folder if folder else ''}",
    )