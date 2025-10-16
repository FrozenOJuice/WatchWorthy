import "./layout.css";
import { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head>
        <title>Movie Review Hub</title>
        <meta name="description" content="Discover movies, read reviews, and share your thoughts" />
      </head>
      <body>
        <header className="header">
          <h1>🎬 Movie Review Hub</h1>
        </header>

        <main className="main-content">
          {children}
        </main>

        <footer className="footer">
          © {new Date().getFullYear()} Movie Review Hub
        </footer>
      </body>
    </html>
  );
}
