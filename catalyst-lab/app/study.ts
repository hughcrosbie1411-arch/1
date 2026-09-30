export type DailyCandle={timestamp:string;open:string;close:string;volume:number};
export function completeSessions(candles:DailyCandle[],cutoff='2026-09-30'){return candles.filter(c=>c.timestamp.slice(0,10)<cutoff)}
export function study(prices:DailyCandle[],bench:Map<string,DailyCandle>,date:string,timing:string,basis:string){
 const eventIndex=prices.findIndex(c=>c.timestamp.slice(0,10)>=date);
 if(!prices.length||eventIndex<0||date<prices[0].timestamp.slice(0,10))return {error:'Date is outside the complete daily snapshot.',rows:[]};
 const sameDay=prices[eventIndex].timestamp.slice(0,10)===date;
 const entryIndex=eventIndex+(sameDay&&timing==='after'?1:0);
 const entry=prices[entryIndex],pre=prices[entryIndex-1];
 if(!entry||!pre)return {error:'Insufficient complete sessions around this event.',rows:[]};
 const start=basis==='reaction'?Number(pre.close):Number(entry.open),bstart=bench.get((basis==='reaction'?pre:entry).timestamp.slice(0,10));
 if(!bstart)return {error:'Benchmark entry session is missing.',rows:[]};
 const bp=Number(basis==='reaction'?bstart.close:bstart.open);
 return {error:'',entry:entry.timestamp.slice(0,10),baseline:(basis==='reaction'?pre:entry).timestamp.slice(0,10),rows:[1,3,5,10,20].map(h=>{const end=prices[entryIndex+h-1],be=end?bench.get(end.timestamp.slice(0,10)):undefined;if(!end||!be)return {h,stock:null,benchmark:null,excess:null,end:'Pending'};const sr=(Number(end.close)/start-1)*100,br=(Number(be.close)/bp-1)*100;return {h,stock:sr,benchmark:br,excess:sr-br,end:end.timestamp.slice(0,10)};})};
}
