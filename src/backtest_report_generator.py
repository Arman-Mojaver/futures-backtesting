from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class BacktestReportGenerator:
    NANOSECONDS = 1e10
    MILLISECONDS = 1e3

    LEFT_MARGIN = 72
    RIGHT_MARGIN = 72
    TOP_MARGIN = 72
    BOTTOM_MARGIN = 72

    def __init__(self):
        pass

    @staticmethod
    def ns_to_dt(ns: Any) -> datetime | None:  # noqa: ANN401
        if ns is None:
            return None
        try:
            sec = float(ns) / 1e9
            return datetime.fromtimestamp(sec, tz=timezone.utc)
        except Exception:  # noqa: BLE001
            return None

    def pretty_duration(self, elapsed: Any) -> str:  # noqa: ANN401
        try:
            e = float(elapsed)
        except Exception:  # noqa: BLE001
            return str(elapsed)

        if e > self.NANOSECONDS:
            td = timedelta(seconds=e / 1e9)
        elif e > self.MILLISECONDS:
            td = timedelta(milliseconds=e)
        else:
            td = timedelta(seconds=e)

        total_seconds = int(td.total_seconds())
        days, rem = divmod(total_seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        parts = []

        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        return " ".join(parts)

    @staticmethod
    def fmt_value(v: Any) -> str:  # noqa: ANN401
        if isinstance(v, float):
            return f"{v:,.6g}"
        return str(v)

    def build_meta_lines(self, data: dict[str, Any]) -> list[tuple[str, str]]:
        run_start_dt = self.ns_to_dt(data.get("run_started"))
        run_finished_dt = self.ns_to_dt(data.get("run_finished"))
        backtest_start_dt = self.ns_to_dt(data.get("backtest_start"))
        backtest_end_dt = self.ns_to_dt(data.get("backtest_end"))

        return [
            ("Run ID", data.get("run_id")),
            ("Trader ID", data.get("trader_id")),
            ("Instance ID", data.get("instance_id")),
            ("Machine ID", data.get("machine_id")),
            ("Run Config ID", data.get("run_config_id")),
            ("Run started (UTC)", run_start_dt.isoformat() if run_start_dt else "N/A"),
            (
                "Run finished (UTC)",
                run_finished_dt.isoformat() if run_finished_dt else "N/A",
            ),
            (
                "Backtest start (UTC)",
                backtest_start_dt.isoformat() if backtest_start_dt else "N/A",
            ),
            (
                "Backtest end (UTC)",
                backtest_end_dt.isoformat() if backtest_end_dt else "N/A",
            ),
            (
                "Elapsed (best-effort)",
                self.pretty_duration(data.get("elapsed_time")),
            ),
            ("Iterations", str(data.get("iterations"))),
            ("Total Events", str(data.get("total_events"))),
            ("Total Orders", str(data.get("total_orders"))),
            ("Total Positions", str(data.get("total_positions"))),
        ]

    @staticmethod
    def _create_intro(data: dict[str, Any], styles: StyleSheet1) -> list[Any]:
        intro = (
            "This document summarizes the results of a backtest run "
            f"(ID: {data.get('run_id')}). The run was executed by trader "
            f"'{data.get('trader_id')}' on machine '{data.get('machine_id')}' "
            f"(instance {data.get('instance_id')}). Below you'll find high-level "
            "metadata, performance statistics and a brief table of key PnL and "
            "returns metrics.\n"
        )
        return [
            Paragraph("Backtest Report", styles["Title"]),
            Spacer(1, 12),
            Paragraph(intro.replace("\n", "<br/>"), styles["BodyText"]),
            Spacer(1, 12),
        ]

    @staticmethod
    def _create_meta_table(meta_lines: list[tuple[str, str]]) -> object:
        rows = [[k, v] for k, v in meta_lines]
        table = Table(rows, hAlign="LEFT", colWidths=[5.5 * cm, 9.5 * cm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (1, 0), colors.whitesmoke),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.gray),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        return table

    def _create_pnl_tables(
        self,
        pnls: dict[str, dict[str, Any]],
        styles: StyleSheet1,
    ) -> list[Any]:
        flow = []
        for currency, metrics in pnls.items():
            flow.append(Paragraph(f"PnL Statistics ({currency})", styles["Heading2"]))
            table_data = [["Metric", "Value"]]
            for k, v in metrics.items():
                table_data.append([k, self.fmt_value(v)])
            t = Table(table_data, hAlign="LEFT", colWidths=[7.5 * cm, 7.5 * cm])
            t.setStyle(
                TableStyle(
                    [
                        ("BOX", (0, 0), (-1, -1), 0.25, colors.gray),
                        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                        ("BACKGROUND", (0, 0), (1, 0), colors.whitesmoke),
                    ]
                )
            )
            flow.append(t)
            flow.append(Spacer(1, 15))
        return flow

    @staticmethod
    def _create_returns_table(
        returns: dict[str, Any],
        styles: StyleSheet1,
    ) -> list:
        flow = [Paragraph("Returns Metrics", styles["Heading2"])]
        table_data = [["Metric", "Value"]]
        for k, v in returns.items():
            table_data.append([k, BacktestReportGenerator.fmt_value(v)])
        t = Table(table_data, hAlign="LEFT", colWidths=[7.5 * cm, 7.5 * cm])
        t.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.gray),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                    ("BACKGROUND", (0, 0), (1, 0), colors.whitesmoke),
                ]
            )
        )
        flow.append(t)
        return flow

    def generate(self, data: dict[str, Any], file_path: Path) -> None:
        if not isinstance(data, dict):
            err = "data must be a dict"
            raise TypeError(err)

        if not isinstance(file_path, Path):
            err = "file_path must be a Path"
            raise TypeError(err)

        doc = SimpleDocTemplate(
            str(file_path),
            pagesize=letter,
            leftMargin=self.LEFT_MARGIN,
            rightMargin=self.RIGHT_MARGIN,
            topMargin=self.TOP_MARGIN,
            bottomMargin=self.BOTTOM_MARGIN,
        )
        styles = getSampleStyleSheet()

        story = []
        story.extend(self._create_intro(data, styles))

        meta_lines = self.build_meta_lines(data)
        story.append(self._create_meta_table(meta_lines))

        pnls = data.get("stats_pnls", {})
        story.extend(self._create_pnl_tables(pnls, styles))

        returns = data.get("stats_returns", {})
        story.extend(self._create_returns_table(returns, styles))

        doc.build(story)
