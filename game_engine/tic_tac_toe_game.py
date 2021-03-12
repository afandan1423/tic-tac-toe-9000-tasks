from copy import deepcopy
from typing import Callable, List, Optional
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
            winner_id=self.__winner_id,
        )
        for turn in self.__turns:
            if turn.player_id == self.__first_player_id:
                ch = "X"
            else:
                ch = "O"
            result.field[turn.x_coordinate][turn.y_coordinate] = ch
        if result.winner_id == "":
            draw_check = [""] * 8
            y = result.field
            for a in range(len(y)):
                x = [""] * len(y)
                for l in range(len(x)):
                    x[l] = y[l][a]
                if x.count(" ") == 0:
                    if x[0] == "X":
                        result.winner_id = result.first_player_id
                    elif x[0] == "O":
                        result.winner_id = result.second_player_id
                elif y[a].count(" ") == 0:
                    if y[a][0] == "X":
                        result.winner_id = result.first_player_id
                    elif y[a][0] == "O":
                        result.winner_id = result.second_player_id
                if x.count("X") > 0 and x.count("O") > 0:
                    draw_check[a*2] = "True"
                if y[a].count("X") > 0 and y[a].count("O") > 0:
                    draw_check[a*2 + 1] = "True"
            m, n = [""] * len(y), [""] * len(y)
            for k in range(len(y)):
                m[k] = y[k][k]
                n[k] = y[k][len(y) - k]
            if m.count("") == 0:
                if m[1] == "X":
                    result.winner_id = result.first_player_id
                elif m[1] == "O":
                    result.winner_id = result.second_player_id
                elif m.count("X") > 0 and m.count("O") > 0:
                    draw_check[7] = "True"
            if n.count("") == 0:
                if n[1] == "X":
                    result.winner_id = result.first_player_id
                elif n[1] == "O":
                    result.winner_id = result.second_player_id
                elif n.count("X") > 0 and n.count("O") > 0:
                    draw_check[8] = "True"
            if draw_check.count("True") == 8:
                result.winner_id = "Draw"
        return result