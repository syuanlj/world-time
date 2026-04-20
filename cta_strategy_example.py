#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CTA 策略示例
基于 vnpy CTA 策略模块的双均线策略实现
"""

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


class DoubleMaStrategy(CtaTemplate):
    """双均线 CTA 策略"""
    
    author = "VeighNa Trader"

    # 策略参数
    fixed_size = 1          # 固定交易手数
    ma_window = 20          # 均线周期
    enter_long_bar_count = 5   # 金叉后开多等待的 K 线数
    exit_long_bar_count = 10   # 死叉后平多等待的 K 线数

    # 策略变量
    ma_value = 0.0          # 当前均线值
    bar_count = 0           # K 线计数
    is_long = False         # 是否持有多单
    
    parameters = ["fixed_size", "ma_window", "enter_long_bar_count", "exit_long_bar_count"]
    variables = ["ma_value", "bar_count", "is_long"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        
        # 创建 K 线合成器和数据管理器
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager(size=self.ma_window + 10)  # 预留缓冲空间

    def on_init(self):
        """策略初始化回调"""
        self.write_log("策略初始化")
        # 加载历史数据用于初始化指标
        self.load_bar(10)

    def on_start(self):
        """策略启动回调"""
        self.write_log("策略启动")

    def on_stop(self):
        """策略停止回调"""
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """Tick 数据更新回调"""
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """K 线数据更新回调"""
        # 更新数据管理器
        self.am.update_bar(bar)
        
        # 检查数据是否足够
        if not self.am.inited:
            return
        
        # 计算均线
        ma_array = self.am.sma(self.ma_window, array=True)
        if len(ma_array) < 2:
            return
            
        current_ma = ma_array[-1]
        previous_ma = ma_array[-2]
        
        # 判断金叉死叉
        cross_over = (current_ma > previous_ma and 
                      ma_array[-3] <= ma_array[-4] if len(ma_array) >= 4 else False)
        cross_below = (current_ma < previous_ma and 
                       ma_array[-3] >= ma_array[-4] if len(ma_array) >= 4 else False)
        
        # 金叉：准备开多
        if cross_over:
            self.bar_count = 0
            self.is_long = True
            self.write_log(f"金叉信号，准备开多")
        
        # 死叉：准备平多
        elif cross_below:
            self.bar_count = 0
            self.is_long = False
            self.write_log(f"死叉信号，准备平多")
        
        # 执行交易逻辑
        if self.is_long and self.bar_count == self.enter_long_bar_count:
            # 开多
            self.buy(bar.close_price, self.fixed_size)
            self.write_log(f"开多成交：价格={bar.close_price}, 数量={self.fixed_size}")
            
        elif not self.is_long and self.bar_count == self.exit_long_bar_count:
            # 平多
            self.sell(bar.close_price, self.fixed_size)
            self.write_log(f"平多成交：价格={bar.close_price}, 数量={self.fixed_size}")
        
        # 更新 K 线计数
        self.bar_count += 1
        self.ma_value = current_ma
        
        # 更新图形显示
        self.put_event()

    def on_order(self, order: OrderData):
        """订单状态更新回调"""
        pass

    def on_trade(self, trade: TradeData):
        """成交状态更新回调"""
        self.write_log(f"成交：方向={trade.direction}, 价格={trade.price}, 数量={trade.volume}")
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """停止单状态更新回调"""
        pass
