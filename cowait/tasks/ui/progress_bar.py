from .ui_component import UIComponent


class ProgressBar(UIComponent):
    def __init__(self, task, id, value: float, min: float, max: float, label: str = ''):
        super().__init__(task, id, '@cowait/ProgressBar')
        self.state = {
            'value': value,
            'min': min,
            'max': max,
            'label': label,
        }

    async def set_value(self, value):
        await self.set('value', value)

    async def set_min(self, value):
        await self.set('min', value)

    async def set_max(self, value):
        await self.set('max', value)

    async def set_label(self, value):
        await self.set('label', value)

