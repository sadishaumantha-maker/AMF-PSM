"""Anatomical Market Framework (AMF) -- structural / diagnostic modelling toolkit.

This package is a software implementation of the *analytical method* of the
Anatomical Market Framework: it models a market as the seven anatomical systems,
the dependency and feedback graph that couples them, and computes structural
diagnostics and shock-propagation simulations over that anatomy.

It is **not** a trading system. There are no orders, brokers, prices, returns,
P&L, signals, or backtests anywhere in this package; every quantity it produces
describes market *structure and resilience*.

This is an illustrative, educational tool. Its inputs, thresholds, and scores are
not empirically validated, are not financial, investment, or trading advice, and
do not constitute a diagnosis, forecast, or prediction of any real or live market.
"""

from __future__ import annotations

from amf.diagnostics import DiagnosticConfig, DiagnosticEngine
from amf.errors import (
    AMFError,
    IncompleteMarketError,
    InvalidConfigError,
    InvalidDependencyError,
    InvalidShockError,
    InvalidSystemError,
    MarketParseError,
)
from amf.graph import CouplingMatrix, DependencyGraph
from amf.market import Market
from amf.models import (
    ChangeMode,
    Dependency,
    DependencyKind,
    DiagnosticReport,
    Intervention,
    LeveragePoint,
    MarketBoundary,
    MetricStats,
    PolicyLayer,
    PolicyProfile,
    PolicyTier,
    ResilienceDistribution,
    ResilienceScore,
    Sensitivity,
    SensitivityReport,
    Severity,
    Shock,
    SimulationTrace,
    SystemKind,
    SystemMetric,
    WeaknessFinding,
)
from amf.policy import PolicyStack
from amf.sensitivity import SensitivityAnalyzer, SensitivityConfig
from amf.simulation import ShockSimulator, SimulationConfig
from amf.systems import (
    SYSTEM_FACTORIES,
    AnatomicalSystem,
    circulatory,
    immune,
    metabolism,
    musculature,
    nervous,
    organs,
    skeleton,
)

__version__ = "0.1.0"

__all__ = [
    "SYSTEM_FACTORIES",
    "AMFError",
    "AnatomicalSystem",
    "ChangeMode",
    "CouplingMatrix",
    "Dependency",
    "DependencyGraph",
    "DependencyKind",
    "DiagnosticConfig",
    "DiagnosticEngine",
    "DiagnosticReport",
    "IncompleteMarketError",
    "Intervention",
    "InvalidConfigError",
    "InvalidDependencyError",
    "InvalidShockError",
    "InvalidSystemError",
    "LeveragePoint",
    "Market",
    "MarketBoundary",
    "MarketParseError",
    "MetricStats",
    "PolicyLayer",
    "PolicyProfile",
    "PolicyStack",
    "PolicyTier",
    "ResilienceDistribution",
    "ResilienceScore",
    "Sensitivity",
    "SensitivityAnalyzer",
    "SensitivityConfig",
    "SensitivityReport",
    "Severity",
    "Shock",
    "ShockSimulator",
    "SimulationConfig",
    "SimulationTrace",
    "SystemKind",
    "SystemMetric",
    "WeaknessFinding",
    "__version__",
    "circulatory",
    "immune",
    "metabolism",
    "musculature",
    "nervous",
    "organs",
    "skeleton",
]
