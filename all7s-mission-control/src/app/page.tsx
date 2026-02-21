import Link from "next/link";

export default function Home() {
  return (
    <div>
      <h1>All7s Mission Control</h1>
      <p className="muted">Choose a module from the left menu.</p>
      <div className="home-links">
        <Link href="/cron" className="home-card">
          Open Cron Calendar
        </Link>
        <Link href="/strategy-review" className="home-card">
          Open Canasta Strategy Review
        </Link>
      </div>
    </div>
  );
}
