class EscGameError(Exception):
    ...


class ConfigurationError(EscGameError):

    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotFoundError(EscGameError):
    ...


class ObjectNotFoundError(NotFoundError):

    object_name: str

    def __init__(self, object_name: str) -> None:
        self.object_name = object_name
        super().__init__(f"Object {object_name} not found.")


class PropertyNotFoundError(NotFoundError):

    object_name: str
    property_name: str

    def __init__(self, object_name: str, property_name: str) -> None:
        self.object_name = object_name
        self.property_name = property_name
        super().__init__(f"Object {object_name} has no property {property_name}.")


class ActionNotFoundError(NotFoundError):

    object_name: str
    action_name: str

    def __init__(self, object_name: str, action_name: str) -> None:
        self.object_name = object_name
        self.action_name = action_name
        super().__init__(f"Object {object_name} has no action {action_name}.")


class RoomPackNotFoundError(NotFoundError):

    room_name: str

    def __init__(self, room_name: str) -> None:
        self.room_name = room_name
        super().__init__(f"Room {room_name} not found.")

