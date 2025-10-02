"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import { useDebounce } from "@/hooks/useDebounce";

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/feed", label: "Feed" },
  { href: "/compose", label: "Compose" },
  { href: "/profile/me", label: "Profile" },
  { href: "/login", label: "Login" },
];

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const [query, setQuery] = useState("");
  const debounced = useDebounce(query, 300);

  useEffect(() => {
    if (debounced.trim()) {
      router.push(`/search?q=${encodeURIComponent(debounced.trim())}`);
    }
  }, [debounced, router]);

  return (
    <header className="bg-white shadow">
      <nav className="container mx-auto flex items-center justify-between px-4 py-3">
        {/* Brand */}
        <Link href="/" className="text-xl font-bold text-blue-600">
          Socially
        </Link>

        {/* Nav Links */}
        <ul className="flex space-x-4 items-center">
          {navLinks.map((link) => (
            <li key={link.href}>
              <Link
                href={link.href}
                className={`${
                  pathname === link.href
                    ? "text-blue-600 font-semibold"
                    : "text-gray-600 hover:text-blue-500"
                }`}
              >
                {link.label}
              </Link>
            </li>
          ))}
          {/* Search box */}
          <li>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search..."
              className="ml-4 rounded-md border border-gray-300 px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </li>
        </ul>
      </nav>
    </header>
  );
}
