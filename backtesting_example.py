#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
回测示例脚本
使用 vnpy CTA 回测模块对双均线策略进行历史回测
"""

from datetime import datetime
from vnpy_ctastrategy.backtesting import BacktestingEngine, OptimizationSetting
from vnpy.trader.constant import Interval
from cta_strategy_example import DoubleMaStrategy


def run_backtesting():
    """运行回测"""
    # 创建回测引擎
    engine = BacktestingEngine()
    
    # 配置回测参数
    engine.set_parameters(
        vt_symbol="IF0.CFFEX",        # 合约代码（沪深 300 股指期货主力连续）
        interval=Interval.MINUTE,     # K 线周期：分钟线
        start=datetime(2026, 4, 15),  # 回测开始日期（使用实际数据日期）
        end=datetime(2026, 4, 21),    # 回测结束日期
        rate=0.0001,                  # 手续费率
        slippage=0.2,                 # 滑点设置
        size=300,                     # 合约乘数
        pricetick=0.2,                # 最小价格变动
        capital=1_000_000,            # 初始资金
        annual_interest_rate=0.03,    # 年化利率
    )
    
    # 添加策略
    engine.add_strategy(DoubleMaStrategy, {})
    
    # 加载数据
    print("正在加载历史数据...")
    engine.load_data()
    
    # 运行回测
    print("正在运行回测...")
    engine.run_backtesting()
    
    # 计算结果
    df = engine.calculate_result()
    statistics = engine.calculate_statistics()
    
    # 打印统计结果
    print("\n" + "="*50)
    print("回测统计结果")
    print("="*50)
    for key, value in statistics.items():
        print(f"{key}: {value}")
    
    # 显示图表
    print("\n生成回测图表...")
    engine.show_chart()
    
    return statistics


def run_optimization():
    """运行参数优化"""
    # 创建回测引擎
    engine = BacktestingEngine()
    
    # 配置回测参数
    engine.set_parameters(
        vt_symbol="IF0.CFFEX",        # 合约代码（沪深 300 股指期货主力连续）
        interval=Interval.MINUTE,     # K 线周期：分钟线
        start=datetime(2026, 4, 15),  # 回测开始日期
        end=datetime(2026, 4, 21),    # 回测结束日期
        rate=0.0001,                  # 手续费率
        slippage=0.2,                 # 滑点设置
        size=300,                     # 合约乘数
        pricetick=0.2,                # 最小价格变动
        capital=1_000_000,            # 初始资金
    )
    
    # 添加策略
    engine.add_strategy(DoubleMaStrategy, {})
    
    # 配置优化参数
    setting = OptimizationSetting()
    setting.set_target("sharpe_ratio")  # 优化目标：夏普比率
    setting.add_parameter("ma_window", 10, 30, 5)           # 均线周期范围
    setting.add_parameter("enter_long_bar_count", 3, 7, 2)  # 入场等待期范围
    
    # 运行优化
    print("正在运行参数优化...")
    results = engine.run_optimization(setting, output=True)
    
    # 打印优化结果
    print("\n" + "="*50)
    print("参数优化结果")
    print("="*50)
    for result in results[:5]:  # 显示前 5 个最优结果
        print(f"参数：{result[0]}, 夏普比率：{result[1]:.4f}")
    
    return results


if __name__ == "__main__":
    # 运行回测
    # statistics = run_backtesting()
    
    # 运行参数优化
    results = run_optimization()
