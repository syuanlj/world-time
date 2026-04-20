#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VeighNa Trader 启动脚本
基于 vnpy 框架构建的量化交易程序入口
"""

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

# 导入网关（根据实际需求启用）
# from vnpy_ctp import CtpGateway
# from vnpy_ctptest import CtptestGateway
# from vnpy_mini import MiniGateway
# from vnpy_femas import FemasGateway
# from vnpy_sopt import SoptGateway
# from vnpy_uft import UftGateway
# from vnpy_esunny import EsunnyGateway
# from vnpy_xtp import XtpGateway
# from vnpy_tora import ToraStockGateway, ToraOptionGateway
# from vnpy_ib import IbGateway
# from vnpy_tap import TapGateway
# from vnpy_da import DaGateway
# from vnpy_rohon import RohonGateway
# from vnpy_tts import TtsGateway

# 导入应用模块
# from vnpy_paperaccount import PaperAccountApp
from vnpy_ctastrategy import CtaStrategyApp
from vnpy_ctabacktester import CtaBacktesterApp
# from vnpy_spreadtrading import SpreadTradingApp
# from vnpy_algotrading import AlgoTradingApp
# from vnpy_optionmaster import OptionMasterApp
# from vnpy_portfoliostrategy import PortfolioStrategyApp
# from vnpy_scripttrader import ScriptTraderApp
# from vnpy_chartwizard import ChartWizardApp
# from vnpy_rpcservice import RpcServiceApp
# from vnpy_excelrtd import ExcelRtdApp
from vnpy_datamanager import DataManagerApp
# from vnpy_datarecorder import DataRecorderApp
# from vnpy_riskmanager import RiskManagerApp
# from vnpy_webtrader import WebTraderApp
# from vnpy_portfoliomanager import PortfolioManagerApp


def main():
    """主函数：启动 VeighNa Trader"""
    # 创建 Qt 应用
    qapp = create_qapp()

    # 创建事件引擎
    event_engine = EventEngine()

    # 创建主引擎
    main_engine = MainEngine(event_engine)

    # 添加网关（根据实际交易接口选择）
    # main_engine.add_gateway(CtpGateway)  # CTP 期货接口
    # main_engine.add_gateway(MiniGateway)  # 迷你期货接口
    # main_engine.add_gateway(XtpGateway)   # XTP 证券接口
    # main_engine.add_gateway(IbGateway)    # IB 国际接口
    
    # 添加应用模块
    # main_engine.add_app(PaperAccountApp)      # 模拟交易
    main_engine.add_app(CtaStrategyApp)         # CTA 策略
    main_engine.add_app(CtaBacktesterApp)       # CTA 回测
    # main_engine.add_app(SpreadTradingApp)     # 价差交易
    # main_engine.add_app(AlgoTradingApp)       # 算法交易
    # main_engine.add_app(PortfolioStrategyApp) # 组合策略
    main_engine.add_app(DataManagerApp)         # 数据管理
    # main_engine.add_app(RiskManagerApp)       # 风险管理

    # 创建并显示主窗口
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    # 运行应用
    qapp.exec()


if __name__ == "__main__":
    main()
