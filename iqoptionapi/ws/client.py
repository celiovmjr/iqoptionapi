"""Module for IQ Option WebSocket client."""

import json
import logging
import ssl
from threading import Thread

import websocket
import certifi

import iqoptionapi.constants as OP_code
import iqoptionapi.global_value as global_value
from iqoptionapi.ws.received.technical_indicators import technical_indicators
from iqoptionapi.ws.received.time_sync import time_sync
from iqoptionapi.ws.received.heartbeat import heartbeat
from iqoptionapi.ws.received.balances import balances
from iqoptionapi.ws.received.profile import profile
from iqoptionapi.ws.received.balance_changed import balance_changed
from iqoptionapi.ws.received.candles import candles
from iqoptionapi.ws.received.buy_complete import buy_complete
from iqoptionapi.ws.received.option import option
from iqoptionapi.ws.received.position_history import position_history
from iqoptionapi.ws.received.list_info_data import list_info_data
from iqoptionapi.ws.received.candle_generated import candle_generated_realtime
from iqoptionapi.ws.received.candle_generated_v2 import candle_generated_v2
from iqoptionapi.ws.received.commission_changed import commission_changed
from iqoptionapi.ws.received.socket_option_opened import socket_option_opened
from iqoptionapi.ws.received.api_option_init_all_result import api_option_init_all_result
from iqoptionapi.ws.received.initialization_data import initialization_data
from iqoptionapi.ws.received.underlying_list import underlying_list
from iqoptionapi.ws.received.instruments import instruments
from iqoptionapi.ws.received.financial_information import financial_information
from iqoptionapi.ws.received.position_changed import position_changed
from iqoptionapi.ws.received.option_opened import option_opened
from iqoptionapi.ws.received.option_closed import option_closed
from iqoptionapi.ws.received.top_assets_updated import top_assets_updated
from iqoptionapi.ws.received.strike_list import strike_list
from iqoptionapi.ws.received.api_game_betinfo_result import api_game_betinfo_result
from iqoptionapi.ws.received.traders_mood_changed import traders_mood_changed
from iqoptionapi.ws.received.order import order
from iqoptionapi.ws.received.position import position
from iqoptionapi.ws.received.positions import positions
from iqoptionapi.ws.received.order_placed_temp import order_placed_temp
from iqoptionapi.ws.received.deferred_orders import deferred_orders
from iqoptionapi.ws.received.history_positions import history_positions
from iqoptionapi.ws.received.available_leverages import available_leverages
from iqoptionapi.ws.received.order_canceled import order_canceled
from iqoptionapi.ws.received.position_closed import position_closed
from iqoptionapi.ws.received.overnight_fee import overnight_fee
from iqoptionapi.ws.received.api_game_getoptions_result import api_game_getoptions_result
from iqoptionapi.ws.received.sold_options import sold_options
from iqoptionapi.ws.received.tpsl_changed import tpsl_changed
from iqoptionapi.ws.received.auto_margin_call_changed import auto_margin_call_changed
from iqoptionapi.ws.received.digital_option_placed import digital_option_placed
from iqoptionapi.ws.received.result import result
from iqoptionapi.ws.received.instrument_quotes_generated import instrument_quotes_generated
from iqoptionapi.ws.received.training_balance_reset import training_balance_reset
from iqoptionapi.ws.received.socket_option_closed import socket_option_closed
from iqoptionapi.ws.received.live_deal_binary_option_placed import live_deal_binary_option_placed
from iqoptionapi.ws.received.live_deal_digital_option import live_deal_digital_option
from iqoptionapi.ws.received.leaderboard_deals_client import leaderboard_deals_client
from iqoptionapi.ws.received.live_deal import live_deal
from iqoptionapi.ws.received.user_profile_client import user_profile_client
from iqoptionapi.ws.received.leaderboard_userinfo_deals_client import leaderboard_userinfo_deals_client
from iqoptionapi.ws.received.client_price_generated import client_price_generated
from iqoptionapi.ws.received.users_availability import users_availability


class WebsocketClient:
    """Handles IQ Option WebSocket communication."""

    def __init__(self, api):
        """Initialize the WebSocket client."""
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

    def dict_queue_add(self, store, max_size, key1, key2, key3, value):
        """Add value to nested dictionary with size limit."""
        subdict = store.setdefault(key1, {}).setdefault(key2, {})
        if key3 in subdict:
            subdict[key3] = value
        elif len(subdict) < max_size:
            subdict[key3] = value
        else:
            oldest_key = sorted(subdict.keys())[0]
            del subdict[oldest_key]
            subdict[key3] = value

    def api_dict_clean(self, obj):
        """Clear dictionary if it exceeds size limit."""
        if len(obj) > 5000:
            obj.pop(next(iter(obj)))

    def on_message(self, ws, message):
        """Handle incoming WebSocket messages."""
        global_value.ssl_Mutual_exclusion = True
        logging.getLogger(__name__).debug(message)
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            return

        technical_indicators(self.api, data, self.api_dict_clean)
        time_sync(self.api, data)
        heartbeat(self.api, data)
        balances(self.api, data)
        profile(self.api, data)
        balance_changed(self.api, data)
        candles(self.api, data)
        buy_complete(self.api, data)
        option(self.api, data)
        position_history(self.api, data)
        list_info_data(self.api, data)
        candle_generated_realtime(self.api, data, self.dict_queue_add)
        candle_generated_v2(self.api, data, self.dict_queue_add)
        commission_changed(self.api, data)
        socket_option_opened(self.api, data)
        api_option_init_all_result(self.api, data)
        initialization_data(self.api, data)
        underlying_list(self.api, data)
        instruments(self.api, data)
        financial_information(self.api, data)
        position_changed(self.api, data)
        option_opened(self.api, data)
        option_closed(self.api, data)
        top_assets_updated(self.api, data)
        strike_list(self.api, data)
        api_game_betinfo_result(self.api, data)
        traders_mood_changed(self.api, data)
        order_placed_temp(self.api, data)
        order(self.api, data)
        position(self.api, data)
        positions(self.api, data)
        deferred_orders(self.api, data)
        history_positions(self.api, data)
        available_leverages(self.api, data)
        order_canceled(self.api, data)
        position_closed(self.api, data)
        overnight_fee(self.api, data)
        api_game_getoptions_result(self.api, data)
        sold_options(self.api, data)
        tpsl_changed(self.api, data)
        auto_margin_call_changed(self.api, data)
        digital_option_placed(self.api, data, self.api_dict_clean)
        result(self.api, data)
        instrument_quotes_generated(self.api, data)
        training_balance_reset(self.api, data)
        socket_option_closed(self.api, data)
        live_deal_binary_option_placed(self.api, data)
        live_deal_digital_option(self.api, data)
        leaderboard_deals_client(self.api, data)
        live_deal(self.api, data)
        user_profile_client(self.api, data)
        leaderboard_userinfo_deals_client(self.api, data)
        users_availability(self.api, data)
        client_price_generated(self.api, data)

        global_value.ssl_Mutual_exclusion = False

    @staticmethod
    def on_error(ws, error):
        """Handle WebSocket errors."""
        logging.getLogger(__name__).error(f"WebSocket error: {error}")
        global_value.websocket_error_reason = str(error)
        global_value.check_websocket_if_error = True

    @staticmethod
    def on_open(ws):
        """Handle WebSocket open event."""
        logging.getLogger(__name__).info("WebSocket connection opened.")
        global_value.check_websocket_if_connect = 1

    @staticmethod
    def on_close(ws, close_status_code, close_msg):
        """Handle WebSocket close event."""
        logging.getLogger(__name__).warning(f"WebSocket closed: {close_status_code} - {close_msg}")
        global_value.check_websocket_if_connect = 0

    def run_forever(self):
        """Run the WebSocket client in a background thread."""
        sslopt = {
            "check_hostname": True,
            "cert_reqs": ssl.CERT_REQUIRED,
            "ca_certs": certifi.where(),
        }
        thread = Thread(target=self.wss.run_forever, kwargs={"sslopt": sslopt})
        thread.daemon = True
        thread.start()
