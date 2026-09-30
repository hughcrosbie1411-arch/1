import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'Catalyst Lab · Event research', description: 'Source-backed daily event studies for catalyst research.' };
export default function Layout({children}:{children:React.ReactNode}) {return <html lang="en"><body>{children}</body></html>}
