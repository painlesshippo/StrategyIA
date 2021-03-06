import math

import time

from RULEngine.Debug.debug_interface import DebugInterface
from RULEngine.Util.Position import Position
from RULEngine.Util.geometry import get_distance, get_angle
from ai.STA.Action.Idle import Idle
from ai.STA.Tactic.Tactic import Tactic
from ai.STA.Tactic.tactic_constants import Flags
from ai.Util.Raycast import raycast

MAX_WIDTH_TO_PASS = 100
ANGLE_TO_ITER = 0.2


class StandOutWaitPass(Tactic):

    def __init__(self, game_state, player_id, target, args):
        super().__init__(game_state, player_id, target, args)

        self.current_state = self.stand_out
        self.next_state = self.stand_out
        self.kicker_id = int(args[0])
        self.debug = DebugInterface()
        self.time_waiting = time.time()

    def stand_out(self) -> None:
        self.status_flag = Flags.WIP

        if self.am_i_standing_out():
            self.next_state = self.wait_for_pass
        else:
            self.next_state = self.stand_out
        return Idle(self.game_state, self.player_id)

    def am_i_standing_out(self) -> bool:
        player_pos = self.game_state.get_player_position(self.player_id)
        kicker_pos = self.game_state.get_player_position(self.kicker_id)
        distance_to_kicker = get_distance(player_pos, kicker_pos)
        angle_kicker_to_player = get_angle(kicker_pos, player_pos)
        is_standing_out = raycast(self.game_state, kicker_pos, distance_to_kicker, angle_kicker_to_player,
                                  MAX_WIDTH_TO_PASS, [self.player_id, self.kicker_id], [], True)

        self.debug.add_log(1, str(not is_standing_out))
        return not is_standing_out

    def find_possibles_standin_out_positions(self):
        kicker_posi = self.game_state.get_player_position(self.kicker_id)
        distance_to_kicker = get_distance(self.game_state.get_player_position(self.player_id), kicker_posi)
        increment_multiplier = 1
        clear_position = []
        #pente, ordonne
        #while



    def wait_for_pass(self):
        self.next_state = self.wait_for_pass
        return Idle(self.game_state, self.player_id)
