import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-center">
      <h1 className="text-4xl sm:text-6xl font-bold mb-6">
        Welcome to <span className="text-blue-600">Socially</span>
      </h1>
      <p className="text-lg text-gray-600 dark:text-gray-300 mb-10 max-w-2xl">
        A modern social blogging platform to share your thoughts, connect with others, and stay inspired.
      </p>
      <div className="flex gap-4">
        <Link
          href="/register"
          className="px-6 py-3 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition"
        >
          Get Started
        </Link>
        <Link
          href="/login"
          className="px-6 py-3 rounded-lg border border-gray-300 dark:border-gray-700 font-medium hover:bg-gray-100 dark:hover:bg-gray-800 transition"
        >
          Login
        </Link>
      </div>
    </div>
  );
}
