#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据下载脚本
使用 AkShare 下载期货历史数据并保存到数据库
"""

import akshare as ak
from datetime import datetime, timedelta
from vnpy.trader.database import get_database
from vnpy.trader.object import BarData
from vnpy.trader.constant import Exchange, Interval
from typing import List


def download_futures_bars(
    symbol: str = "IF0", 
    exchange: str = "CFFEX",
    start_date: str = "20230101",
    end_date: str = "20231231",
    interval: str = "1m"
) -> List[BarData]:
    """
    下载期货历史 K 线数据
    
    Args:
        symbol: 品种代码，如 IF（沪深 300 股指期货）
        exchange: 交易所代码，如 CFFEX
        start_date: 开始日期，格式 YYYYMMDD
        end_date: 结束日期，格式 YYYYMMDD
        interval: K 线周期，支持 1m/5m/15m/30m/60m/d
    
    Returns:
        BarData 列表
    """
    print(f"正在下载 {symbol} {interval} K 线数据...")
    print(f"日期范围：{start_date} - {end_date}")
    
    # 调用 AkShare 获取期货历史数据
    try:
        # 下载分钟线数据
        if interval in ["1m", "5m", "15m", "30m", "60m"]:
            # 使用 futures_zh_minute_sina 接口
            df = ak.futures_zh_minute_sina(symbol=symbol, period=interval)
        elif interval == "d":
            # 使用 futures_zh_daily_sina 接口
            df = ak.futures_zh_daily_sina(symbol=symbol)
        else:
            raise ValueError(f"不支持的 K 线周期：{interval}")
        
        print(f"下载完成，共 {len(df)} 条数据")
        print(df.head())
        
        # 转换为 BarData 对象
        bars = []
        for idx, row in df.iterrows():
            # 解析时间
            if isinstance(row['datetime'], str):
                dt = datetime.strptime(row['datetime'], "%Y-%m-%d %H:%M:%S")
            else:
                dt = row['datetime']
            
            # 创建 BarData 对象
            bar = BarData(
                symbol=symbol,
                exchange=Exchange(exchange),
                datetime=dt,
                interval=Interval.MINUTE if interval != "d" else Interval.DAILY,
                volume=row.get('volume', 0),
                turnover=row.get('turnover', 0),
                open_interest=row.get('open_interest', 0),
                open_price=row.get('open', 0),
                high_price=row.get('high', 0),
                low_price=row.get('low', 0),
                close_price=row.get('close', 0),
                gateway_name="akshare"
            )
            bars.append(bar)
        
        return bars
        
    except Exception as e:
        print(f"下载数据失败：{e}")
        return []


def save_to_database(bars: List[BarData], chunk_size: int = 1000):
    """批量保存数据到数据库"""
    if not bars:
        print("没有数据需要保存")
        return
    
    db = get_database()
    total = len(bars)
    saved = 0
    
    print(f"\n开始保存 {total} 条数据到数据库...")
    
    for i in range(0, total, chunk_size):
        chunk = bars[i:i+chunk_size]
        if db.save_bar_data(chunk):
            saved += len(chunk)
            print(f"已保存 {saved}/{total} 条数据")
    
    print(f"数据保存完成，共保存 {saved} 条数据")


def main():
    """主函数"""
    print("="*60)
    print("期货历史数据下载工具")
    print("="*60)
    
    # 下载沪深 300 股指期货主力连续合约数据
    # 注意：AkShare 的主力连续合约数据需要使用特定格式
    # IF0 表示沪深 300 股指期货主力连续
    
    bars = download_futures_bars(
        symbol="IF0",  # 沪深 300 股指期货主力连续
        exchange="CFFEX",
        start_date="20230101",
        end_date="20231231",
        interval="1m"
    )
    
    if bars:
        save_to_database(bars)
        
        # 验证数据
        db = get_database()
        loaded_bars = db.load_bar_data(
            symbol="IF0",
            exchange=Exchange.CFFEX,
            interval=Interval.MINUTE,
            start=datetime(2023, 1, 1),
            end=datetime(2023, 12, 31)
        )
        print(f"\n验证：从数据库加载了 {len(loaded_bars)} 条数据")
    else:
        print("数据下载失败，请检查网络连接或参数设置")


if __name__ == "__main__":
    main()
