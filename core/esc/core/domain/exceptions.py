class EcsGameError(Exception):
    ...


class ObjectNotInteractable(EcsGameError):

    object_name: str

    def __init__(self, object_name: str) -> None:
        self.object_name = object_name
        super().__init__(f"Object not interactable")
