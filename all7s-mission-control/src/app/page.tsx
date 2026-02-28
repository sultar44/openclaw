import Link from "next/link";

export default function Home() {
  return (
    <div>
      <h1>All7s Mission Control</h1>
      <p className="muted">Choose a module from the left menu.</p>
      <div className="home-links">
        <Link href="/strategy-review" className="home-card">
          Open Canasta Strategy Review
        </Link>
        <Link href="/better-hand" className="home-card">
          Open Better Hand Emails
        </Link>
        <Link href="/sunday-ritual" className="home-card">
          Open Sunday Ritual
        </Link>
      </div>
    </div>
  );
}
