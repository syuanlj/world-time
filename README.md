# VeighNa Trader 量化交易系统

基于 [vnpy](https://github.com/vnpy/vnpy) 框架构建的量化交易程序。

## 项目结构

```
/workspace
├── vnpy/                       # VnPy 核心框架代码
│   ├── event/                  # 事件引擎模块
│   ├── trader/                 # 交易引擎模块
│   ├── chart/                  # K 线图表模块
│   ├── rpc/                    # RPC 通信模块
│   └── alpha/                  # Alpha 研究模块
├── examples/                   # 官方示例代码
│   ├── veighna_trader/         # 主交易程序示例
│   ├── cta_backtesting/        # CTA 回测示例
│   ├── portfolio_backtesting/  # 组合回测示例
│   └── ...                     # 其他示例
├── run.py                      # 主程序启动脚本
├── cta_strategy_example.py     # CTA 策略示例（双均线）
├── backtesting_example.py      # 回测示例脚本
└── README.md                   # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
# 安装 VnPy 核心包
pip install vnpy

# 安装 CTA 策略模块
pip install vnpy-ctastrategy vnpy-ctabacktester

# 安装数据管理模块
pip install vnpy-datamanager

# 安装数据库支持（SQLite）
pip install vnpy-sqlite

# 根据需求安装交易接口网关
# pip install vnpy-ctp        # CTP 期货接口
# pip install vnpy-xtp        # XTP 证券接口
# pip install vnpy-ib         # IB 国际接口
```

### 2. 启动交易程序

```bash
python run.py
```

### 3. 运行回测

```bash
python backtesting_example.py
```

## 核心组件

### 事件引擎 (EventEngine)
负责处理系统内所有事件的调度和分发，是 VnPy 的核心组件之一。

### 主引擎 (MainEngine)
整合所有功能模块，提供统一的 API 接口，管理网关、应用、数据等。

### 交易网关 (Gateway)
连接不同交易接口的适配器，目前已支持：
- CTP（国内期货）
- XTP（证券）
- IB（国际）
- Mini（迷你期货）
- 更多接口请参考官方文档

### 应用模块 (App)
- **CtaStrategy**: CTA 自动交易策略
- **CtaBacktester**: CTA 策略回测
- **DataManager**: 历史数据管理
- **PortfolioStrategy**: 组合策略交易
- **RiskManager**: 风险管理
- 更多应用请参考官方文档

## 策略开发

### 创建自定义策略

继承 `CtaTemplate` 类并实现以下回调方法：

```python
from vnpy_ctastrategy import CtaTemplate, BarData, TickData

class MyStrategy(CtaTemplate):
    author = "Your Name"
    
    # 策略参数
    parameters = ["param1", "param2"]
    
    # 策略变量
    variables = ["var1", "var2"]
    
    def on_init(self):
        """策略初始化"""
        self.write_log("策略初始化")
        self.load_bar(10)  # 加载 10 天历史数据
    
    def on_start(self):
        """策略启动"""
        self.write_log("策略启动")
    
    def on_stop(self):
        """策略停止"""
        self.write_log("策略停止")
    
    def on_tick(self, tick: TickData):
        """Tick 更新"""
        pass
    
    def on_bar(self, bar: BarData):
        """K 线更新 - 主要交易逻辑"""
        pass
    
    def on_order(self, order):
        """订单状态更新"""
        pass
    
    def on_trade(self, trade):
        """成交更新"""
        pass
```

### 策略交易函数

- `buy(price, volume)`: 买入开仓
- `sell(price, volume)`: 卖出平仓
- `short(price, volume)`: 卖出开仓（做空）
- `cover(price, volume)`: 买入平仓（平空）
- `cancel_all()`: 撤销所有活动委托

## 回测系统

### 配置回测参数

```python
from vnpy_ctastrategy.backtesting import BacktestingEngine
from datetime import datetime

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="IF888.CFFEX",      # 合约代码
    interval="1m",                # K 线周期
    start=datetime(2023, 1, 1),   # 开始日期
    end=datetime(2023, 12, 31),   # 结束日期
    rate=0.0001,                  # 手续费率
    slippage=0.2,                 # 滑点
    size=300,                     # 合约乘数
    pricetick=0.2,                # 最小价格变动
    capital=1_000_000,            # 初始资金
)
```

### 参数优化

使用网格搜索或遗传算法进行参数优化：

```python
from vnpy_ctastrategy.backtesting import OptimizationSetting

setting = OptimizationSetting()
setting.set_target("sharpe_ratio")  # 优化目标
setting.add_parameter("ma_window", 10, 30, 5)

# 网格搜索
results = engine.run_optimization(setting, use_ga=False)

# 遗传算法
# results = engine.run_optimization(setting, use_ga=True)
```

## 数据管理

### 下载数据

使用 DataManager 应用或命令行工具下载历史数据。

### 数据存储

VnPy 支持多种数据库：
- SQLite（轻量级，默认）
- MySQL
- PostgreSQL
- MongoDB
- DolphinDB

## 风险管理

### 内置风控功能

- 单笔委托数量限制
- 总持仓数量限制
- 撤单频率限制
- 成交数量限制
- 账户盈亏限制

### 自定义风控规则

通过 `RiskManagerApp` 添加自定义风控规则。

## 部署建议

### 生产环境配置

1. **服务器选择**: 选择靠近交易所机房的云服务器
2. **网络稳定性**: 确保网络连接稳定可靠
3. **备份机制**: 配置数据备份和灾难恢复方案
4. **监控告警**: 设置系统监控和异常告警

### 注意事项

⚠️ **重要提示**:
- 实盘交易前务必充分回测和模拟测试
- 从小资金开始逐步验证策略有效性
- 做好风险管理和资金管理
- 定期检查系统运行状态
- 关注交易所规则变化

## 资源链接

- [VnPy 官方文档](https://www.vnpy.com/docs)
- [VnPy GitHub](https://github.com/vnpy/vnpy)
- [VnPy 社区论坛](https://www.vnpy.com/forum)
- [CTA 策略教程](https://www.vnpy.com/docs/cta_strategy.html)

## 许可证

本项目基于 MIT 许可证开源，详见 [LICENSE](https://github.com/vnpy/vnpy/blob/master/LICENSE)。

## 免责声明

本代码仅供学习和研究使用，不构成任何投资建议。量化交易存在风险，入市需谨慎。使用本系统进行实盘交易的一切后果由使用者自行承担。
