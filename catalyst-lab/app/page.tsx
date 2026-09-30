import Dashboard from './dashboard';
import {readFile} from 'node:fs/promises';
export const dynamic='force-dynamic';
export default async function Page(){
 try {const [nke,spy]=await Promise.all(['NKE.US','SPY.US'].map(s=>readFile(`${process.cwd()}/data/${s}.json`,'utf8').then(JSON.parse)));if(!nke.candles?.some((c:{timestamp:string})=>c.timestamp.slice(0,10)<"2026-09-30")||!spy.candles?.length)throw new Error("Empty snapshot");return <Dashboard stock={nke} benchmark={spy}/>}
 catch {return <main className="setup"><span className="eyebrow">CATALYST LAB / DATA SETUP</span><h1>Connect your research snapshot.</h1><p>This source repository does not redistribute licensed market data. Import authorized NKE.US and SPY.US daily snapshots to the local data directory to enable the event study dashboard.</p><p>See the repository setup guide. No trading or prediction services are active.</p></main>}
}
