def allow_networking(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.undo()
