export default function Footer() {
  return (
    <footer className="bg-gray-100 border-t py-6 mt-8">
      <div className="container mx-auto text-center text-gray-600 text-sm">
        © {new Date().getFullYear()} Socially. All rights reserved.
        <div className="mt-2">
          <a
            href="/api/docs/"
            className="hover:underline text-blue-600"
          >
            API Docs
          </a>{" "}
          |{" "}
          <a
            href="/api/redoc/"
            className="hover:underline text-blue-600"
          >
            ReDoc
          </a>
        </div>
      </div>
    </footer>
  );
}
