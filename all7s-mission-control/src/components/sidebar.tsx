"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/strategy-review", label: "Canasta Strategy Review" },
  { href: "/better-hand", label: "Better Hand Emails" },
  { href: "/sunday-ritual", label: "Sunday Ritual" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <div className="brand">All7s Mission Control</div>
      <nav className="menu">
        {links.map((link) => {
          const active = pathname.startsWith(link.href);
          return (
            <Link key={link.href} className={`menu-link ${active ? "active" : ""}`} href={link.href}>
              {link.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
