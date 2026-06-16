"""Anatomical Market Framework (AMF) -- structural / diagnostic modelling toolkit.

This package is a software implementation of the *analytical method* of the
Anatomical Market Framework: it models a market as the seven anatomical systems,
the dependency and feedback graph that couples them, and computes structural
diagnostics and shock-propagation simulations over that anatomy.

It is **not** a trading system. There are no orders, brokers, prices, returns,
P&L, signals, or backtests anywhere in this package; every quantity it produces
describes market *structure and resilience*.
"""

from __future__ import annotations

from amf.diagnostics import DiagnosticConfig, DiagnosticEngine
from amf.errors import (
    AMFError,
    IncompleteMarketError,
    InvalidDependencyError,
    InvalidShockError,
    InvalidSystemError,
    MarketParseError,
)
from amf.graph import CouplingMatrix, DependencyGraph
from amf.market import Market
from amf.models import (
    Dependency,
    DependencyKind,
    DiagnosticReport,
    MarketBoundary,
    ResilienceScore,
    Severity,
    Shock,
    SimulationTrace,
    SystemKind,
    WeaknessFinding,
)
from amf.simulation import ShockSimulator, SimulationConfig
from amf.systems import (
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
    "AMFError",
    "AnatomicalSystem",
    "CouplingMatrix",
    "Dependency",
    "DependencyGraph",
    "DependencyKind",
    "DiagnosticConfig",
    "DiagnosticEngine",
    "DiagnosticReport",
    "IncompleteMarketError",
    "InvalidDependencyError",
    "InvalidShockError",
    "InvalidSystemError",
    "Market",
    "MarketBoundary",
    "MarketParseError",
    "ResilienceScore",
    "Severity",
    "Shock",
    "ShockSimulator",
    "SimulationConfig",
    "SimulationTrace",
    "SystemKind",
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
