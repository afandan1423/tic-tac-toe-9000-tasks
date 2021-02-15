from typing import List, Callable
from copy import deepcopy

from .tic_tac_toe_common_lib import TicTacToeTurn, TicTacToeGameInfo, AbstractTicTacToeGame

class TicTacToeGame(AbstractTicTacToeGame):
    def __init__(
        self,
        game_id: str,
        first_player_id: str,
        second_player_id: str,
        strategy: Callable[[TicTacToeGameInfo], TicTacToeTurn] = None
    ) -> None:
        self.__game_id = game_id
        self.__first_player_id = first_player_id
        self.__second_player_id = second_player_id
        self.__winner_id = ""
        self.__strategy = strategy
        self.__turns: List[TicTacToeTurn] = []

    """пока просто раскладываем по полям"""

    def is_turn_correct(self, turn: TicTacToeTurn) -> bool:
        y = len(self.get_game_info().field)
        if self.get_game_info().winner_id != "":
            return False
        if turn.x_coordinate > y or turn.y_coordinate > y:
            return False
        elif turn.x_coordinate < 0 or turn.y_coordinate < 0:
            return False
        if self.get_game_info().field[turn.x_coordinate][turn.y_coordinate] != " ":
            return False
        z = len(self.get_game_info().sequence_of_turns)
        if z != 0:
            if turn.player_id == self.get_game_info().sequence_of_turns[z - 1].player_id:
                return False
        else:
            if turn.player_id != self.get_game_info().first_player_id:
                return False
        return True

    def do_turn(self, turn: TicTacToeTurn) -> TicTacToeGameInfo:
        if self.is_turn_correct(turn) == False:
            return EnvironmentError
        else:
            self.__turns.append(turn)
            return self.get_game_info()
        """сначала проверяем корректность, для проверки используйте is_turn_correct,
        а возвращаем TicTacToeGameInfo"""

    def get_game_info(self) -> TicTacToeGameInfo:
        result = TicTacToeGameInfo(
            game_id=self.__game_id,
            field=[
                [" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "]
            ],
            sequence_of_turns=deepcopy(self.__turns),
            first_player_id=self.__first_player_id,
            second_player_id=self.__second_player_id,
            winner_id=self.__winner_id
        )
        for turn in self.__turns:
            if turn.player_id == self.__first_player_id:
                ch = "X"
            else:
                ch = "O"
            result.field[turn.x_coordinate][turn.y_coordinate] = ch
        if result.winner_id == "":
            for a in range(len(result.field)):
                x = [""] * len(result.field)
                for y in range(len(x)):
                    x[y] = result.field[y][a]
                if x.count(" ") == 0:
                    if x[0] == "X":
                        result.winner_id = result.first_player_id
                    elif x[0] == "O":
                        result.winner_id = result.second_player_id
                elif result.field[a].count(" ") == 0:
                    if result.field[a][0] == "X":
                        result.winner_id = result.first_player_id
                    elif result.field[a][0] == "O":
                        result.winner_id = result.second_player_id
            x = result.field
            if x[0][0] == x[1][1] == x[2][2] or x[0][0] == x[1][1] == x[2][2]:
                if x[1][1] == "X":
                    result.winner_id = result.first_player_id
                elif x[1][1] == "O":
                    result.winner_id = result.second_player_id
        return result
