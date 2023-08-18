from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)

from vnpy.trader.constant import Interval

from vnpy_ctastrategy.base import Offset
# from vnpyExtend.extendArrayManager_walter import ExtendArrayManager
from vnpyExtend.extendBarData import TradeType
from vnpyExtend.extendArrayManager import ExtendArrayManager
from vnpyExtend.extendBarGenerator import ExtendBarGenerator
from vnpyExtend.extendCtaTemplate import ExtendCtaTemplate


class IntraDayStrategy(ExtendCtaTemplate):
    """
    创建时间: {{_date_}}
    作者: {{_author_}}, {{_email_}}
    策略名称: {{_cursor_}}
    交易逻辑:
    """
    author = '{{_author_}}'

    parameters = []
    variables = []

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        # 通过BarGenerator创建一个instance，其命名通常为bg前缀, 在实盘时，策略引擎调用策略后，首先会调用策略文件中的
        # on_tick()，用实例bg调用方法update_tick(tick)将tick数据合成k线，update_tick根据tick的时间标签判断是否满足
        # 1min（Interval.MINUTE) 或者 1hr(Interval=HOUR)。一旦合成完成将会回调策略函数中on_bar()，这样，在策略中，
        # BarGeneratord的参数interval如果是MINUTE，on_bar就是1分钟k线出现的时刻，如果是HOUR，那么on_bar()就是1小时k线
        # 出现的时刻。在回测时，on_tick()是不被调用的，回测引擎直接调用on_bar()。

        # 下面代码中self.bg_min的命名min只是表示Interval是分钟的k线合成的BarGenerator的实例，无其他特别的意义。
        # 同样，self.bg_hr命名为Hr也只代表Interval小时线的k线合成的BarGenerator的实例，便于区分。

        # 每调用一次on_bar()，把最新获得的单位k线(1mi/1hr)送到 update_bar()中合成多周期k线，具体周期由window确定。
        # 对于指标计算，self.am_min则表示window=对应的ArrayManager实例。当每次k线在BarGenerator中按照on_window_bar
        # 的设置合成一根时间周期为on_window_bar的k线之后，就通过self.am_5min把这个新生成的bar送给其方法update_bar()，
        # 这是通过self.on_5min_bar()中self.am_5min.update_bar()来实现的。在ArrayManager的函数update_bar()中，每收到一个bar，
        # 就会把这个bar添加到一个定长的数组中，由于长度固定，后面进，最早的就丢掉了。

        self.bg_min = ExtendBarGenerator(self.on_bar, window=5, on_window_bar=self.on_mins_bar, interval=Interval.MINUTE)
        self.am_mins = ExtendArrayManager(size=300)
        self.am_mins_heikin = ExtendArrayManager(size=300)

        self.bg_hr = ExtendBarGenerator(self.on_bar, window=1, on_window_bar=self.on_hrs_bar, interval=Interval.HOUR)
        self.am_hrs = ExtendArrayManager(size=100)
        self.am_hrs_heikin = ExtendArrayManager(size=100)

    def on_init(self):
        """ Callback when strategy is inited. """
        self.write_log("策略初始化")
        self.load_bar(20)  # 20天

    def on_start(self):
        """ Callback when strategy is started. """
        self.write_log("策略启动")

    def on_stop(self):
        """ Callback when strategy is stopped. """
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """ Callback of new tick data update. """
        self.bg_min.update_tick(tick)
        self.bg_hr.update_bar(tick)

    def on_bar(self, bar: BarData):
        """cta_engine每分钟回调一次"""
        self.bg_min.update_bar(bar)
        self.bg_hr.update_bar(bar)

    def on_mins_bar(self, bar: BarData):
        """BarGenerator回调函数分钟级别"""
        self.cancel_all()

        self.am_mins.update_bar(bar)
        heikinBar = self.heikin_ashi(bar)
        self.am_mins_heikin.update_bar(heikinBar)

        if not self.am_5min.inited:
            return

        self.put_event()

    def on_hrs_bar(self, bar: BarData):
        """BarGenerator回调函数小时级别"""
        self.am_hrs.update_bar(bar)
        heikinBar = self.heikin_ashi(bar)
        self.am_hrs_heikin.update_bar(heikinBar)

        if not self.am1Hr.inited:
            return

        self._trading(bar, heikinBar)
        self.put_event()

    def _trading(self, bar: BarData, heikinBar: BarData):
        """交易执行"""
        self.cancel_all()

        # 计算指标, 选择下面之一
        # am = self.am_mins
        # am = self.am_hrs

        # 买卖交易
        # self.trade(TradeType.BUY, price, size, comments)
        # self.trade(TradeType.SELL, price, size, comments)
        # self.trade(TradeType.SHORT, price, size, comments)
        # self.trade(TradeType.COVER, price, size, comments)

        data = {
            'gateway_name': bar.gateway_name,
            'extra': bar.extra,
            'symbol': bar.symbol,
            'exchange': bar.exchange.value,
            'datetime': bar.datetime,
            'interval': bar.interval,
            'open_price': bar.open_price,
            'high_price': bar.high_price,
            'low_price': bar.low_price,
            'close_price': bar.close_price,
            'volume': bar.volume,
            # 'candle': {
            #     'boll_up_hr': boll_up_hr, 'boll_lo_hr': boll_low_hr, 'mid_hr': boll_mid_hr,
            #     'boll_up_min': boll_up_min, 'boll_lo_min': boll_up_min, 'mid_min': boll_low_min,
            #     'emaHr': ema_hr[-1], 'buy': buy},
            # 'rsiSma': {'rsi': rsi_hr, 'sma': sma_hr},
            # 'adx': {'adx': adx[-1], 'angle': adx_angle, 'slope': adx_slope},
        }

        self.draw_to_db(data)

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        if trade.offset == Offset.CLOSE and self.pos == 0:
            self.cancel_all()
        trade.comment = self.orderComment.get(trade.vt_orderid)
        self.update_holding_cost(trade)
        self.trade_to_db(trade)
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
