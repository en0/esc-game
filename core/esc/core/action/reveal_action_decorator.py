from typing import List, Optional

from esc.core.typing import Action, ActionApi, InteractionResponseGenerator


class RevealActionDecorator(Action):
    def __init__(self, action: Action) -> None:
        self._action = action

    def get_name(self) -> str:
        return self._action.get_name()

    def get_aliases(self) -> List[str]:
        return self._action.get_aliases()

    def trigger(
            self,
            api: ActionApi,
            using_object: Optional[str],
    ) -> InteractionResponseGenerator:
        name = api.get_owner_name()
        api.reveal_all_child_objects(name)
        yield from self._action.trigger(api, using_object)
