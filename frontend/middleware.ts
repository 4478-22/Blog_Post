import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Public routes accessible without auth
const publicRoutes = ["/", "/login", "/register", "/api", "/_next", "/favicon.ico"];

// Protected routes
const protectedRoutes = ["/feed", "/compose", "/settings"];

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const isPublic = publicRoutes.some((route) => pathname.startsWith(route));
  const isProtected = protectedRoutes.some((route) => pathname.startsWith(route));

  // Read auth flag from cookies (set in login/logout)
  const isAuth = req.cookies.get("auth")?.value === "true";

  if (isProtected && !isAuth) {
    // Redirect unauthenticated users
    const loginUrl = new URL("/login", req.url);
    loginUrl.searchParams.set("redirect", pathname); // optional: redirect back after login
    return NextResponse.redirect(loginUrl);
  }

  if ((pathname === "/login" || pathname === "/register") && isAuth) {
    // Redirect logged-in users away from login/register
    return NextResponse.redirect(new URL("/feed", req.url));
  }

  return NextResponse.next();
}

// Apply middleware to all routes
export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
