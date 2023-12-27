def load_examples(spider_dir: str) -> Tuple[list, list]:
    """Load examples."""
    with open(os.path.join(spider_dir, "train_spider.json")) as f:
        train_spider = json.load(f)
    with open(os.path.join(spider_dir, "train_others.json")) as f:
        train_others = json.load(f)
    with open(os.path.join(spider_dir, "dev.json")) as f:
        dev = json.load(f)
    return train_spider + train_others, dev
