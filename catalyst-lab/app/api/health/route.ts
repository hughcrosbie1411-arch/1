import {access} from 'node:fs/promises';
export async function GET(){const availability=await Promise.all(['NKE.US','SPY.US'].map(async symbol=>{try{await access(`${process.cwd()}/data/${symbol}.json`);return {symbol,available:true}}catch{return {symbol,available:false}}}));return Response.json({status:'ok',mode:'research-only',data:availability,execution:false,predictions:false})}
