import logging
import pykx as kx
from typing import Dict, Any
from mcp_server.utils.kdbx import get_kdb_connection

logger = logging.getLogger(__name__)

async def api_simple_query_impl(ticker: str | list[str], price: float) -> Dict[str, Any]:
    try:
        conn = get_kdb_connection()

        result = conn.mcp.apiCall('.api.simple', [kx.SymbolVector([ticker]) , price])

        if 0==len(result):
            return {"status": "success", "data": [], "message": "No rows returned"}

        # rows = result.py()
        rows = result.pd()

        logger.info(f"Query returned {len(rows)} rows.")
        return {"status": "success", "data": rows}

    except Exception as e:
        logger.error(f"Query failed: {e}")
        return {"status": "error", "message": str(e)}


def register_tools(mcp_server):
    @mcp_server.tool()
    async def kdbx_run_api_simple(inputSym: str | list[str], inputPrice: float) -> Dict[str, Any]:
        """
        Execute an api called '.api.simple' which filters the trade table based on symbol and price. 

        Args:
            inputSym (str | list[str]): A ticker symbol or list of symbols as type string.
            inputPrice (float): A price input that return result greater than the input float.

        Returns:
            Dict[str, Any]: Query execution results.
        """
        return await api_simple_query_impl(ticker=inputSym, price=inputPrice)

    return ['kdbx_run_api_simple']