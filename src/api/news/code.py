from enum import Enum


class NewsType(Enum):
    ECONOMY         = {"name": "경제", "code": "1"}
    POLITICS        = {"name": "정치", "code": "2"}
    ENTERTAINMENT   = {"name": "연예", "code": "3"}
    SPORTS          = {"name": "스포츠", "code": "4"}

    def all_type_list(self):
        return [self.ECONOMY, self.POLITICS, self.ENTERTAINMENT, self.SPORTS]