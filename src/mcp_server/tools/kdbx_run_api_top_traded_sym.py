import logging
import pykx as kx
from typing import Dict, Any
from mcp_server.utils.kdbx import get_kdb_connection

logger = logging.getLogger(__name__)

async def api_top_traded_sym_impl(n: int) -> Dict[str, Any]:
    try:
        conn = get_kdb_connection()

        result = conn.mcp.apiCall('.api.topTradedSym', n)
        if 0==len(result):
            return {"status": "success", "data": [], "message": "No rows returned"}

        rows = result.py()
        # rows = result.pd()
        
        logger.info(f"Query returned {len(rows)} rows.")
        print(rows)
        return {"status": "success", "data": rows}

    except Exception as e:
        logger.error(f"Query failed: {e}")
        return {"status": "error", "message": str(e)}


def register_tools(mcp_server):
    @mcp_server.tool()
    async def kdbx_run_api_top_traded_sym(n: int) -> Dict[str, Any]:
        """
        Execute an api called '.api.topTradedSym' which returns the top traded symbols.

        Args:
            n (int): Number of top traded symbols to return.
          
        Returns:
            str | list[str]: Ticker or list of tickers.
        """
        return await api_top_traded_sym_impl(n)

    return ['kdbx_run_api_top_traded_sym']