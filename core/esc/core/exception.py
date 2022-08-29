class EscGameError(Exception):
    ...


class NotInteractableError(EscGameError):

    object_name: str

    def __init__(self, object_name: str) -> None:
        self.object_name = object_name
        super().__init__(f"Object not interactable")


class NotFoundError(EscGameError):

    object_name: str

    def __init__(self, object_name: str) -> None:
        self.object_name = object_name
        super().__init__(f"Object not found")


class ActionError(EscGameError):

    object_name: str
    action_name: str

    def __init__(self, object_name: str, action_name: str) -> None:
        self.object_name = object_name
        self.action_name = action_name
        super().__init__(f"Unexpected Action Error.")

