
.s.init[]
.ai:use`kx.ai
.logger:use`kx.log
.log:.logger.createLog[]

rows:10000
trade:([]time:.z.d+asc rows?.z.t;sym:rows?`AAPL`GOOG`MSFT`TSLA`AMZN;price:rows?100f;size:rows?1000)

// @example .api.simple[`AAPL`MSFT;10f]
.api.simple:{[s;p] select from trade where sym in s, price > p}

// @example .api.ohlc[`AAPL;1800]
.api.ohlc:{[s;interval] 
    0!select open:first price, high:max price, low:min price, close:last price 
    by time:(0D00:00:01 * interval) xbar time, sym 
    from trade 
    where sym in s}

// @example .api.complex[`sd`ed`tickers`minPrice`maxPrice!(.z.d;.z.d+1;`AAPL`MSFT;10f;100f)]
.api.complex:{[dict] 
    show .dbg.dict:dict;
    select 
    from trade 
    where 
        time.date within dict`sd`ed, 
        sym in dict`tickers, 
        price within dict`minPrice`maxPrice
    }


// @example .mcp.apiCall[`.api.simple;(`AAPL;10f)]
.mcp.apiCall:{[api;args] 
    .log.info("Executing %s with Args: %r";api;args); 
    $[99h = type args;
        res:@[api;args];
        res:api . (),args
        ]; 
    
    if[98h=type res;show 5 sublist res];
    
    :res
    }


// @usage .mcp.listApis[] 
.mcp.listApis:{.Q.dd'[`.api;(key`.api) except `]}  // where type value x is function (100h)


// Next: expand for syms, more flexibility with price ?

// api with dictionary input `sd`ed`tickers`minPrice`maxPrice!(sd;ed;syms;minPrice;maxPrice) 
// timestamps inputs 