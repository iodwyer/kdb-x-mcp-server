import logging
import pykx as kx
from typing import Dict, Any
from mcp_server.utils.kdbx import get_kdb_connection

logger = logging.getLogger(__name__)

async def api_simple_ohlc_impl(ticker: str | list[str], timeInterval: int) -> Dict[str, Any]:
    try:
        conn = get_kdb_connection()
        ticker = kx.SymbolAtom(ticker) if isinstance(ticker, str) else kx.SymbolVector(ticker) if isinstance(ticker, list) and all(isinstance(s, str) for s in ticker) else (_ for _ in ()).throw(TypeError("Expected str or list[str]"))

        result = conn.mcp.apiCall('.api.ohlc', [ticker, timeInterval])
        if 0==len(result):
            return {"status": "success", "data": [], "message": "No rows returned"}

        rows = result.py()
        # rows = result.pd()

        logger.info(f"Query returned {len(rows)} rows.")
        return {"status": "success", "data": rows}

    except Exception as e:
        logger.error(f"Query failed: {e}")
        return {"status": "error", "message": str(e)}


def register_tools(mcp_server):
    @mcp_server.tool()
    async def kdbx_run_api_ohlc(inputSym: str | list[str], inputTimeInterval: int) -> Dict[str, Any]:
        """
        Execute an api called '.api.ohlc' which Performs an Open, High, Low, Close (OHLC) on the trade table 
        filtering by sym (ticker) and grouping by second time intervals.

        Args:
            inputSym (str | list[str]): A ticker symbol or list of symbols as type string.
            inputTimeInterval (int): A time interval in seconds to group the OHLC data.

        Returns:
            Dict[str, Any]: Query execution results.
        """
        return await api_simple_ohlc_impl(ticker=inputSym, timeInterval=inputTimeInterval)

    return ['kdbx_run_api_ohlc']