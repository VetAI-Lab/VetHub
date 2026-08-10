from vethub.io import ROOT, load_yaml


def test_seed_registry_has_unique_full_names():
    payload = load_yaml(ROOT / "registry" / "repositories.yaml")
    names = [item["full_name"].lower() for item in payload["resources"]]
    assert len(names) == len(set(names))


def test_seed_registry_entries_have_core_fields():
    payload = load_yaml(ROOT / "registry" / "repositories.yaml")

    for item in payload["resources"]:
        assert item["id"]
        assert item["source"]
        assert item["full_name"]
        assert item["url"].startswith("https://")
